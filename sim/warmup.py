"""
Build-time warmup. Runs once during the image build to (1) download and bake
Isaac Sim's kit extensions + shader cache into the image so runtime cold starts
are ~30s instead of minutes, (2) cache the Unitree G1 asset, and (3) VERIFY the
RTX renderer actually produces frames on this GPU (the shapes printed below are
the proof). Output goes to stderr so it survives Isaac Sim's stdout hijack.
"""
import sys
import numpy as np


def log(*a):
    print("[warmup]", *a, file=sys.stderr, flush=True)


from isaacsim.simulation_app import SimulationApp
sim_app = SimulationApp({"headless": True, "width": 1280, "height": 720})

from isaacsim.core.api import World
from isaacsim.core.utils.stage import add_reference_to_stage
try:
    from isaacsim.storage.native import get_assets_root_path
except Exception:
    from omni.isaac.nucleus import get_assets_root_path
from isaacsim.sensors.camera import Camera
import omni.client

world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()

root = get_assets_root_path()
log("assets root:", root)
for c in [
    root + "/Isaac/Robots/Unitree/G1/g1.usd",
    root + "/Isaac/Robots/Unitree/G1/g1_minimal.usd",
    root + "/Isaac/IsaacLab/Robots/Unitree/G1/g1.usd",
    root + "/Isaac/Robots/Unitree/G1/G1.usd",
]:
    try:
        r, _ = omni.client.stat(c)
        if r == omni.client.Result.OK:
            add_reference_to_stage(usd_path=c, prim_path="/World/G1")
            log("G1 found + cached:", c)
            break
    except Exception as e:
        log("stat failed", c, e)
else:
    log("G1 USD not found at known paths (stream will use fallback marker)")

cam = Camera(prim_path="/World/cam", position=np.array([3.0, 3.0, 2.0]), resolution=(1280, 720))
world.reset()
cam.initialize()

ok = 0
for i in range(50):
    world.step(render=True)
    rgba = cam.get_rgba()
    if i % 10 == 0 or i == 49:
        shape = None if rgba is None else getattr(rgba, "shape", "n/a")
        nonzero = bool(rgba is not None and rgba.size and rgba[..., :3].any())
        log(f"frame {i}: rgba={shape} has_pixels={nonzero}")
        if nonzero:
            ok += 1

log(f"RENDER VERIFIED: {ok} sampled frames had pixels" if ok else "RENDER PRODUCED NO PIXELS")
log("warmup done — caches baked")
sim_app.close()
