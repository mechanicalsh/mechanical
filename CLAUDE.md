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

- **The humanoid sim is Governor's proving ground** — where the governor layer
  physically vetoes a humanoid's actuators. That demo *is* the thesis on camera before
  any silicon exists. It started as Isaac-Sim-on-Modal research in the Oryx session but
  is being pulled into Governor as standalone.
- **Stack call: use MuJoCo, not Isaac-Sim-on-Modal.** Isaac Sim's RTX renderer segfaults
  on headless cloud GPUs (NGX/DLSS init). You do not need photoreal rendering to
  demonstrate a safety veto. The Unitree G1 ships in MuJoCo Menagerie and runs locally
  on Apple Silicon, free. Keep Isaac Sim as a later "pretty render" only.
- **Unresolved:** whether the proving-ground code lands here under `governorbot` (the
  recommendation) or a robomart-ai repo. Confirm with the user before importing any
  sim code that was built against Robomart's Modal/NVIDIA credentials.

## Conventions

- Naming is locked: company/chip = **Governor**, open layer = **Govern Protocol**
  (noun and verb). Identity primitive = **Sequence** (WIP), registry = Robotkind (WIP).
  Don't reintroduce the dozens of rejected candidate names.
- Writing voice for any outward doc: plain, concrete, no jargon. The founder reacts
  hard to em-dashes, colons-as-drama, and "X, not Y" negation constructions — avoid them.
- When building any marketing site, default to **Mechanical UI** (the house design
  system at `~/mechanical-ui/`) unless told otherwise.
