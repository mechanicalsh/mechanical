"""
humanoid-lab — Unitree G1 in NVIDIA Isaac Sim, on a Modal L40S GPU.

Goal: stand up Isaac Sim headless on a cloud GPU, load the Unitree G1, and let
the robot move about (locomotion), recorded to video. GR00T smoke test is a
separate function (manipulation brain — it does not drive locomotion).

Run order (cheap -> expensive):
  modal run app.py::sysinfo     # proves image + GPU + Isaac Sim launch (M2/M3)
  modal run app.py::walk        # G1 locomotion, records mp4 (M4)

Notes:
  - L40S has ray-tracing cores. Isaac Sim rendering needs them; A100/H100 do not.
  - Modal orchestrates in its own python and shells out to Isaac Sim's bundled
    python (/isaac-sim/python.sh) so client deps never collide with Isaac Sim's.
"""
import modal

ISAAC_SIM_TAG = "nvcr.io/nvidia/isaac-sim:4.5.0"
ISAACLAB_REF = "v2.1.0"  # pinned to match Isaac Sim 4.5.0
GPU = "L40S"

# Build-time env: accept the EULAs non-interactively, or Isaac Sim blocks on a prompt.
EULA_ENV = {
    "ACCEPT_EULA": "Y",
    "PRIVACY_CONSENT": "Y",
    "OMNI_KIT_ACCEPT_EULA": "YES",
}

isaac_image = (
    modal.Image.from_registry(
        ISAAC_SIM_TAG,
        secret=modal.Secret.from_name("ngc-registry"),  # REGISTRY_USERNAME/PASSWORD for nvcr.io
        add_python="3.11",  # clean python for the Modal entrypoint; sim runs via python.sh
    )
    .env(EULA_ENV)
    .apt_install("git", "cmake", "build-essential", "ffmpeg", "libgl1")
    .run_commands(
        # Isaac Lab clone + install into Isaac Sim's bundled python.
        f"git clone --depth 1 -b {ISAACLAB_REF} https://github.com/isaac-sim/IsaacLab.git /root/IsaacLab",
        "ln -sf /isaac-sim /root/IsaacLab/_isaac_sim",
        "cd /root/IsaacLab && ./isaaclab.sh --install rsl_rl",
        gpu=GPU,  # attach a GPU for the install (some extensions JIT/cache against the driver)
    )
)

app = modal.App("humanoid-lab")
outputs = modal.Volume.from_name("humanoid-lab-outputs", create_if_missing=True)

# Streaming image: append to the cached Isaac image (PIL+aiohttp into Isaac Sim's
# python), then mount the live stream server. Editing stream_server.py does not
# trigger an image rebuild.
stream_image = (
    isaac_image
    # Isaac Sim's RTX renderer needs graphics+display driver caps, not just compute.
    # Without these the Vulkan device is lost the moment it renders.
    .env({
        "NVIDIA_DRIVER_CAPABILITIES": "all",
        "NVIDIA_VISIBLE_DEVICES": "all",
        "PYTHONUNBUFFERED": "1",
    })
    .run_commands("/isaac-sim/python.sh -m pip install Pillow aiohttp")
    # Bake the kit-extension + shader cache (and the G1 asset) into the image at
    # build time so runtime cold starts are ~30s, not minutes. Also verifies the
    # renderer produces pixels (see the [warmup] lines in the build log).
    .add_local_file("warmup.py", "/root/warmup.py", copy=True)
    .run_commands("/isaac-sim/python.sh /root/warmup.py || true", gpu=GPU)
    .add_local_file("stream_server.py", "/root/stream_server.py")
)


@app.function(image=stream_image, gpu=GPU, timeout=900, volumes={"/outputs": outputs})
def render_test(renderer: str = "RayTracedLighting", disable_dlss: bool = True):
    """Staged bisect of the renderer. Stage markers go to the OUTPUT VOLUME with an
    immediate commit, so they survive both Isaac Sim's stdout hijack AND a segfault.
    Read /outputs/rt_progress.txt afterward; the last line is exactly where it died."""
    import os
    import numpy as np

    os.makedirs("/outputs", exist_ok=True)
    open("/outputs/rt_progress.txt", "w").close()
    outputs.commit()

    def mark(s):
        with open("/outputs/rt_progress.txt", "a") as f:
            f.write(s + "\n")
        outputs.commit()

    mark(f"stage0: launching SimulationApp (renderer={renderer}, disable_dlss={disable_dlss})")
    cfg = {"headless": True, "renderer": renderer}
    from isaacsim.simulation_app import SimulationApp
    sim = SimulationApp(cfg)
    mark("stage1: SimulationApp UP")

    if disable_dlss:
        # the crash lands right after NGX/DLSS init — try turning the neural path off
        import carb
        s = carb.settings.get_settings()
        for k, v in [("/rtx/post/dlss/execMode", 0), ("/rtx-transient/dlssg/enabled", False),
                     ("/rtx/newDenoiser/enabled", False), ("/rtx/reflections/enabled", False)]:
            try:
                s.set(k, v)
            except Exception as e:
                mark(f"  setting {k} failed: {e}")
        mark("stage1b: DLSS/NGX settings applied")

    from isaacsim.core.api import World
    w = World(stage_units_in_meters=1.0)
    w.scene.add_default_ground_plane()
    w.reset()
    mark("stage2: world+ground OK; physics WITHOUT render")
    for _ in range(30):
        w.step(render=False)
    mark("stage3: physics-only OK; now stepping WITH render")
    for _ in range(30):
        w.step(render=True)
    mark("stage4: render-step OK; creating Camera")
    from isaacsim.sensors.camera import Camera
    cam = Camera(prim_path="/World/cam", position=np.array([3.0, 3.0, 2.0]), resolution=(640, 480))
    cam.initialize()
    mark("stage5: camera init OK; get_rgba loop")
    from PIL import Image
    saved = False
    for i in range(90):
        w.step(render=True)
        rgba = cam.get_rgba()
        if rgba is not None and rgba.size and rgba[..., :3].any():
            Image.fromarray(rgba[:, :, :3].astype("uint8")).save("/outputs/test_frame.png")
            mark(f"stage6: SAVED test_frame.png at frame {i}")
            outputs.commit()
            saved = True
            break
    mark(f"DONE saved={saved}")
    sim.close()
    return f"render_test done, saved={saved}"


@app.function(image=stream_image, gpu=GPU, timeout=3600, secrets=[modal.Secret.from_name("ngc-api")])
@modal.concurrent(max_inputs=100)
@modal.web_server(8000, startup_timeout=600)
def stream():
    """Live browser stream: launch Isaac Sim + the G1 + the orbiting camera, served on :8000."""
    import subprocess
    subprocess.Popen(["/isaac-sim/python.sh", "/root/stream_server.py"])


@app.function(image=isaac_image, gpu=GPU, timeout=1800)
def sysinfo():
    """M2/M3: prove the image built, the GPU is visible, Isaac Sim launches, and the G1 task is registered."""
    import subprocess

    print("=== nvidia-smi ===", flush=True)
    subprocess.run("nvidia-smi", shell=True)

    print("\n=== Isaac Sim headless launch + physics step ===", flush=True)
    check = r'''
from isaacsim.simulation_app import SimulationApp
app = SimulationApp({"headless": True})
import isaacsim.core.utils.stage as stage_utils
from isaacsim.core.api import World
w = World(stage_units_in_meters=1.0)
w.scene.add_default_ground_plane()
w.reset()
for _ in range(60):
    w.step(render=False)
print("ISAAC_SIM_OK: stepped physics 60 frames headless")
app.close()
'''
    with open("/root/_check.py", "w") as f:
        f.write(check)
    subprocess.run("/isaac-sim/python.sh /root/_check.py", shell=True, check=True)

    print("\n=== Unitree G1 locomotion tasks registered in Isaac Lab ===", flush=True)
    subprocess.run(
        "cd /root/IsaacLab && ./isaaclab.sh -p scripts/environments/list_envs.py 2>/dev/null | grep -i g1 || true",
        shell=True,
    )
    return "sysinfo complete"


@app.function(image=isaac_image, gpu=GPU, timeout=3600, volumes={"/outputs": outputs})
def walk(iterations: int = 300, num_envs: int = 1024, task: str = "Isaac-Velocity-Flat-G1-v0"):
    """M4: train the G1 locomotion policy headless with video capture. The recorded
    mp4 (the ego moving about) is copied to the output volume and returned as bytes."""
    import subprocess, glob, os, shutil

    cmd = (
        "cd /root/IsaacLab && ./isaaclab.sh -p "
        "scripts/reinforcement_learning/rsl_rl/train.py "
        f"--task {task} --headless --video --video_length 300 --video_interval {max(iterations - 50, 25)} "
        f"--max_iterations {iterations} --num_envs {num_envs}"
    )
    print("RUN:", cmd, flush=True)
    subprocess.run(cmd, shell=True, check=True)

    vids = sorted(glob.glob("/root/IsaacLab/logs/**/videos/**/*.mp4", recursive=True), key=os.path.getmtime)
    print("videos found:", vids, flush=True)
    if not vids:
        return None
    latest = vids[-1]
    os.makedirs("/outputs", exist_ok=True)
    dest = "/outputs/g1_walk.mp4"
    shutil.copy(latest, dest)
    outputs.commit()
    with open(latest, "rb") as f:
        return f.read()


@app.local_entrypoint()
def main(mode: str = "sysinfo", iterations: int = 300):
    if mode == "sysinfo":
        print(sysinfo.remote())
    elif mode == "walk":
        data = walk.remote(iterations=iterations)
        if data:
            with open("g1_walk.mp4", "wb") as f:
                f.write(data)
            print(f"wrote g1_walk.mp4 ({len(data)/1e6:.1f} MB)")
        else:
            print("no video produced")
