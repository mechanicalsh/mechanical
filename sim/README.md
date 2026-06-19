# sim — Governor's proving ground

Where the governor layer is demonstrated: a humanoid in simulation whose actuators
the safety governor can physically veto. This is the thesis on camera before any
silicon exists.

Started as Isaac-Sim-on-Modal research; being carried into Governor as standalone.

## What's here (Isaac Sim path)

- `app.py` — Modal app. Builds an Isaac Sim 4.5.0 + Isaac Lab image on an L40S.
  - `sysinfo` — proves the image built, GPU visible, Isaac Sim launches headless, G1 task registered.
  - `walk` — trains the G1 locomotion policy headless and records the robot moving to mp4.
  - `render_test` — staged renderer bisect; markers written to the output volume so they survive a segfault.
  - `stream` — live browser view over a WebSocket (see `stream_server.py`).
- `stream_server.py` — boots Isaac Sim, loads the G1, orbits a camera, JPEG-streams frames to the browser.
- `warmup.py` — build-time cache bake + a render-verification pass.
- `onstart.sh` — VM-style bootstrap (note: still curls a stream_server from a roboalias gist — replace before reuse).

## Status / known wall

Isaac Sim's **RTX renderer segfaults on headless cloud GPUs** (crash lands at NGX/DLSS
init). Compute and physics run fine; rendering does not. Reproduced multiple ways on
Modal L40S. `render_test` was the bisect that pinned it.

## Forward direction: MuJoCo, not Isaac-on-Modal

For the Governor demo (governor vetoes actuators) you do not need photoreal RTX. The
**Unitree G1 ships in MuJoCo Menagerie** and runs locally on Apple Silicon, free, with
full actuator control — trivial to clamp or zero a joint command the moment a rule
trips, and easy to record. That is the right substrate for the veto demo. Keep the
Isaac Sim path above as a later "pretty render" only.

## Prerequisites (Isaac path)

- Modal account, authed. `NVIDIA_API_KEY` (NGC) to pull the Isaac Sim container.
- Modal secrets: `ngc-registry` (`REGISTRY_USERNAME=$oauthtoken`, `REGISTRY_PASSWORD=<NGC key>`) and `ngc-api` (`NGC_API_KEY=<NGC key>`).

## Run (Isaac path)

```bash
python3 -m venv .venv && . .venv/bin/activate && pip install modal
modal run app.py::sysinfo      # validates the whole stack
modal run app.py::walk         # records the G1 walking to g1_walk.mp4
```

First run builds the image (~20 GB pull + Isaac Lab install). Later runs reuse the cache.
