"""
Live Isaac Sim -> browser stream. Runs INSIDE the Isaac Sim container (under
/isaac-sim/python.sh). Boots Isaac Sim headless on the GPU, loads the Unitree
G1, renders an orbiting camera, JPEG-encodes each frame, and serves it to the
browser over a WebSocket. The sim runs on the main thread (Isaac Sim is not
thread-safe); the web server runs on a background thread.

Transport is a WebSocket frame stream, not the WebRTC protocol, because Modal's
NAT won't expose the UDP port range native Isaac Sim WebRTC needs. Same result
in the browser: live, interactive, orbiting view.
"""
import os, sys, threading, time, queue, asyncio, io, traceback
import numpy as np

W, H = 1280, 720
TARGET = np.array([0.0, 0.0, 0.7])   # roughly the G1's torso height
PORT = 8000


def log(*a):
    # stderr bypasses Isaac Sim's stdout hijack, so these actually show in Modal logs
    print("[ss]", *a, file=sys.stderr, flush=True)

# ---- shared state between the sim thread and the web thread ----
latest = {"jpg": None, "status": "booting Isaac Sim..."}
controls = queue.Queue()
orbit = {"az": 50.0, "el": 18.0, "r": 3.4, "auto": True}


def mat_to_quat(R):
    """3x3 rotation matrix -> quaternion (w, x, y, z)."""
    t = np.trace(R)
    if t > 0:
        s = np.sqrt(t + 1.0) * 2
        w = 0.25 * s
        x = (R[2, 1] - R[1, 2]) / s
        y = (R[0, 2] - R[2, 0]) / s
        z = (R[1, 0] - R[0, 1]) / s
    elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        s = np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2
        w = (R[2, 1] - R[1, 2]) / s; x = 0.25 * s
        y = (R[0, 1] + R[1, 0]) / s; z = (R[0, 2] + R[2, 0]) / s
    elif R[1, 1] > R[2, 2]:
        s = np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2
        w = (R[0, 2] - R[2, 0]) / s; x = (R[0, 1] + R[1, 0]) / s
        y = 0.25 * s; z = (R[1, 2] + R[2, 1]) / s
    else:
        s = np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2
        w = (R[1, 0] - R[0, 1]) / s; x = (R[0, 2] + R[2, 0]) / s
        y = (R[1, 2] + R[2, 1]) / s; z = 0.25 * s
    return np.array([w, x, y, z])


def look_at_quat(eye, target):
    """Quaternion for a USD camera (forward -Z, up +Y) at `eye` looking at `target`, world up +Z."""
    fwd = target - eye
    fwd = fwd / (np.linalg.norm(fwd) + 1e-9)
    zc = -fwd
    world_up = np.array([0.0, 0.0, 1.0])
    xc = np.cross(world_up, zc)
    if np.linalg.norm(xc) < 1e-6:
        xc = np.array([1.0, 0.0, 0.0])
    xc = xc / np.linalg.norm(xc)
    yc = np.cross(zc, xc)
    R = np.column_stack([xc, yc, zc])
    return mat_to_quat(R)


# ===================== WEB SERVER (background thread) =====================
INDEX_HTML = """<!doctype html><html><head><meta charset=utf-8>
<title>Isaac Sim — Unitree G1 (live)</title>
<style>
 html,body{margin:0;background:#0c0e0d;color:#cdd;font:13px -apple-system,system-ui,sans-serif;height:100%}
 #wrap{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%}
 #v{max-width:96vw;max-height:84vh;border:1px solid #1e4b38;border-radius:6px;background:#000;cursor:grab}
 #bar{margin:10px 0;opacity:.8} b{color:#2ec37a}
 #hint{opacity:.5;font-size:12px;margin-top:4px}
</style></head><body><div id=wrap>
 <div id=bar><b>Isaac Sim</b> · Unitree G1 · live on Modal L40S &nbsp; <span id=s>connecting…</span></div>
 <img id=v width=1280 height=720>
 <div id=hint>drag to orbit · scroll to zoom · double-click to toggle auto-spin</div>
</div><script>
 const img=document.getElementById('v'),s=document.getElementById('s');
 let url=(location.protocol==='https:'?'wss://':'ws://')+location.host+'/ws';
 let ws,last=null;
 function conn(){ ws=new WebSocket(url); ws.binaryType='blob';
   ws.onopen=()=>s.textContent='● live';
   ws.onclose=()=>{s.textContent='reconnecting…';setTimeout(conn,1000);};
   ws.onmessage=e=>{ if(typeof e.data==='string'){s.textContent=e.data;return;}
     const u=URL.createObjectURL(e.data); img.onload=()=>{if(last)URL.revokeObjectURL(last);last=u;}; img.src=u; };
 }
 conn();
 let drag=false,px=0,py=0;
 img.addEventListener('mousedown',e=>{drag=true;px=e.clientX;py=e.clientY;img.style.cursor='grabbing';});
 window.addEventListener('mouseup',()=>{drag=false;img.style.cursor='grab';});
 window.addEventListener('mousemove',e=>{ if(!drag||ws.readyState!=1)return;
   ws.send(JSON.stringify({daz:(e.clientX-px)*0.4,del:-(e.clientY-py)*0.4})); px=e.clientX;py=e.clientY; });
 img.addEventListener('wheel',e=>{e.preventDefault(); if(ws.readyState==1)ws.send(JSON.stringify({dr:e.deltaY*0.002}));},{passive:false});
 img.addEventListener('dblclick',()=>{if(ws.readyState==1)ws.send(JSON.stringify({toggle:true}));});
</script></body></html>"""


def start_web():
    from aiohttp import web

    async def index(_req):
        return web.Response(text=INDEX_HTML, content_type="text/html")

    async def frame(_req):
        if latest["jpg"] is None:
            return web.Response(status=503, text=latest["status"])
        return web.Response(body=latest["jpg"], content_type="image/jpeg")

    async def healthz(_req):
        return web.json_response({"status": latest["status"], "has_frame": latest["jpg"] is not None})

    async def ws_handler(req):
        from aiohttp import WSMsgType
        ws = web.WebSocketResponse(max_msg_size=0)
        await ws.prepare(req)

        async def pump():
            while not ws.closed:
                if latest["jpg"] is not None:
                    try:
                        await ws.send_bytes(latest["jpg"])
                    except Exception:
                        break
                else:
                    try:
                        await ws.send_str(latest["status"])
                    except Exception:
                        break
                await asyncio.sleep(1 / 24)

        task = asyncio.create_task(pump())
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    import json
                    try:
                        controls.put_nowait(json.loads(msg.data))
                    except Exception:
                        pass
        finally:
            task.cancel()
        return ws

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    appw = web.Application()
    appw.add_routes([
        web.get("/", index), web.get("/ws", ws_handler),
        web.get("/frame.jpg", frame), web.get("/healthz", healthz),
    ])
    runner = web.AppRunner(appw)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    loop.run_until_complete(site.start())
    log("web serving on", PORT)
    loop.run_forever()


def _start_web_safe():
    try:
        start_web()
    except Exception:
        log("web thread crashed:\n" + traceback.format_exc())


threading.Thread(target=_start_web_safe, daemon=True).start()
log("module loaded; web thread started")


# ===================== ISAAC SIM (main thread) =====================
def main():
    from isaacsim.simulation_app import SimulationApp
    sim_app = SimulationApp({"headless": True, "width": W, "height": H})

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

    log("isaac imports done; building scene")
    assets_root = get_assets_root_path()
    log("assets root:", assets_root)
    candidates = [
        assets_root + "/Isaac/Robots/Unitree/G1/g1.usd",
        assets_root + "/Isaac/Robots/Unitree/G1/g1_minimal.usd",
        assets_root + "/Isaac/IsaacLab/Robots/Unitree/G1/g1.usd",
        assets_root + "/Isaac/Robots/Unitree/G1/G1.usd",
    ]
    g1 = False
    for c in candidates:
        try:
            res, _ = omni.client.stat(c)
            if res == omni.client.Result.OK:
                add_reference_to_stage(usd_path=c, prim_path="/World/G1")
                log("G1 loaded:", c)
                g1 = True
                break
        except Exception as e:
            log("stat failed", c, e)
    if not g1:
        log("G1 USD not found; spawning a fallback marker")
        from isaacsim.core.api.objects import DynamicCuboid
        world.scene.add(DynamicCuboid(prim_path="/World/Marker",
                                      position=np.array([0, 0, 0.7]),
                                      scale=np.array([0.4, 0.4, 0.4]),
                                      color=np.array([0.91, 0.35, 0.05])))

    cam = Camera(prim_path="/World/StreamCam", resolution=(W, H))
    world.reset()
    cam.initialize()

    from PIL import Image
    log("entering render loop")
    latest["status"] = "rendering…"
    frame = 0
    while sim_app.is_running():
        # apply queued view controls
        while not controls.empty():
            c = controls.get_nowait()
            if c.get("toggle"):
                orbit["auto"] = not orbit["auto"]
            orbit["az"] += float(c.get("daz", 0))
            orbit["el"] = float(np.clip(orbit["el"] + float(c.get("del", 0)), -5, 80))
            orbit["r"] = float(np.clip(orbit["r"] + float(c.get("dr", 0)), 1.2, 9.0))
        if orbit["auto"]:
            orbit["az"] += 0.25

        az, el, r = np.radians(orbit["az"]), np.radians(orbit["el"]), orbit["r"]
        eye = TARGET + np.array([r * np.cos(el) * np.cos(az),
                                 r * np.cos(el) * np.sin(az),
                                 r * np.sin(el)])
        cam.set_world_pose(position=eye, orientation=look_at_quat(eye, TARGET))

        world.step(render=True)

        try:
            rgba = cam.get_rgba()
            if frame < 8:
                log("frame", frame, "rgba", None if rgba is None else getattr(rgba, "shape", "n/a"))
            if rgba is not None and rgba.size > 0:
                buf = io.BytesIO()
                Image.fromarray(rgba[:, :, :3].astype("uint8")).save(buf, "JPEG", quality=80)
                latest["jpg"] = buf.getvalue()
                frame += 1
                if frame in (1, 5, 30) or frame % 240 == 0:
                    log(f"streamed {frame} frames ({len(latest['jpg'])//1024} KB)")
        except Exception as e:
            if frame < 5:
                log("capture err:", e)

    sim_app.close()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        latest["status"] = "sim crashed — see logs"
        time.sleep(3600)  # keep the port up so the browser shows the error
