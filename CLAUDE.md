# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

**Governor Robotics** — brainchips for humanoids. The brain has a conscience that can't
be jailbroken. Two surfaces:

- **Governor** — the company and the governed brainchip. A reasoning layer (any model
  the buyer picks) sits next to a safety governor that holds a *physical veto* over the
  actuators. The laws of robotics as a wire, not a prompt.
- **Govern Protocol** — the open-source software layer: the constitution + admin plane
  for home humanoids. This is what gets open-sourced.

Right now the repo is **docs only** — no application code yet. The canonical docs are
the source of truth; read them before doing strategy or architecture work:

- `README.md` — the thesis, the roadmap sequence, the layer/name stack.
- `DECISIONS.md` — the locked decision log. Append, never rewrite.
- `MOAT.md` — where the defensibility is ("don't sell the circuit, sell the seal").

## Org / push rules — CONTAMINATION WALL (read before any git op)

This is a **syedos-world** project, NOT a Robomart one, despite the robotics theme.

- GitHub org: **`governorbot`**. Repo: `governorbot/governor`.
- Push with **`GITHUB_TOKEN_SYEDOS`** and the **syedos** git identity (already set
  local to this repo: `user.name=syedos`). **Never** use `GITHUB_TOKEN_ROBOALIAS` or a
  robomart-ai/robomind-ai identity here — that cross-contaminates worlds.
- Push pattern used so far (origin is plain HTTPS, so inline the token):
  `git push "https://syedos:${GITHUB_TOKEN_SYEDOS}@github.com/governorbot/governor.git" main`
- **Push to `main` directly. No PRs** (house standing rule). Commit → push → done.

## The thesis, in one breath

Safety must be *physical*. A software constitution can be jailbroken; a silicon one
can't. The whole strategy follows from that. See `MOAT.md` for the full chain, but the
two load-bearing points a future instance must not lose:

1. **The chip's circuit is not the moat** — ARM/NVIDIA could copy a safety
   co-processor in months. The moat is *being the standard*: the test, the cert, the
   registry, and the "Governed" mark that insurers and buyers demand. We are a
   **standard, not a regulator** — no permits, adoption-driven (think UL, Dolby, USB).
2. **The roadmap is a sequence, not a pick:** Govern OS (open software beachhead) →
   safety co-processor on certified ASIL-D silicon (physical veto, zero tapeout) →
   "Governor Inside" certified module → fabless governor die → license the seal. Go
   fabless like ARM; let Thor/Qualcomm be the commodity muscle. Don't ever pitch
   "out-NVIDIA NVIDIA on inference silicon" — that's the explicit trap.

## Open threads (state, so you don't re-litigate)

- **The proving ground lives in its own repo: `governorbot/sim`** (local checkout at
  `~/humanoid-lab`). A Unitree G1 in Isaac Sim where the governor layer will physically
  veto the robot's actuators. That demo *is* the thesis on camera before any silicon
  exists. De-contaminated from roboalias to syedos (identity + gist + token).
- **Rendering runs on Vast.ai (RTX 4090), not Modal.** The wall was Modal-specific: its
  GPU containers ship only the compute driver, so Isaac Sim's RTX renderer segfaults at
  NGX init. Vast rents the whole machine with the full graphics driver, so Isaac Sim
  renders. Rule: A100/H100 have no RT cores — use RTX 4090 / L40 / A6000 for Isaac Sim.
  MuJoCo (G1 in Menagerie, runs locally on Apple Silicon) stays a lighter alternative if
  you only need the veto logic, not the pretty render.
- **Current state:** G1 renders live and streams to the browser; it settles under
  gravity (no controller yet). Next: a locomotion policy to stand/walk, then the governor
  veto layer. See the `governorbot/sim` README.

## Conventions

- Naming is locked: company/chip = **Governor**, open layer = **Govern Protocol**
  (noun and verb). Identity primitive = **Sequence** (WIP), registry = Robotkind (WIP).
  Don't reintroduce the dozens of rejected candidate names.
- Writing voice for any outward doc: plain, concrete, no jargon. The founder reacts
  hard to em-dashes, colons-as-drama, and "X, not Y" negation constructions — avoid them.
- When building any marketing site, default to **Mechanical UI** (the house design
  system at `~/mechanical-ui/`) unless told otherwise.
