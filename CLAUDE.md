# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

**Mechanical, Inc.** — brainchips for humanoids. The brain has a conscience that can't be
jailbroken. The brand is **Mechanical** (full word); **Mech** is the shorthand (chip line,
handles, short link). Two surfaces:

- **The chips (Mech-1, Mech-2, …)** — a reasoning layer (any model the buyer picks) sits
  next to a safety core that holds a *physical veto* over the actuators. Laws of robotics
  as a wire, not a prompt.
- **Mech Protocol** — the open-source software layer: the constitution + admin plane for
  home humanoids. This is what gets open-sourced.

Right now this repo is **docs only** — no application code yet. The canonical docs are the
source of truth; read them before strategy or architecture work:

- `README.md` — the thesis, the roadmap, the name stack.
- `DECISIONS.md` — the locked decision log. Append, never rewrite.
- `MOAT.md` — where the defensibility is ("don't sell the circuit, sell the seal").

## Org / push rules — CONTAMINATION WALL (read before any git op)

This is a **syedos-world** project, NOT a Robomart one, despite the robotics theme.

- GitHub org: **`mechanicalsh`** (renamed from `governorbot`). Repo: `mechanicalsh/mechanical`.
- Push with **`GITHUB_TOKEN_SYEDOS`** and the **syedos** git identity (set local to this
  repo). **Never** use `GITHUB_TOKEN_ROBOALIAS` or a robomart-ai/robomind-ai identity —
  that cross-contaminates worlds.
- Push pattern (origin is plain HTTPS, so inline the token):
  `git push "https://syedos:${GITHUB_TOKEN_SYEDOS}@github.com/mechanicalsh/mechanical.git" main`
- **Push to `main` directly. No PRs** (house standing rule). Commit → push → done.

## The thesis, in one breath

Safety must be *physical*. A software constitution can be jailbroken; a silicon one can't.
See `MOAT.md` for the full chain. Two load-bearing points a future instance must not lose:

1. **The chip's circuit is not the moat** — ARM/NVIDIA could copy a safety co-processor in
   months. The moat is *being the standard*: the test, the cert, the registry, and the Mech
   seal that insurers and buyers demand. We are a **standard, not a regulator** — no
   permits, adoption-driven (UL, Dolby, USB).
2. **The roadmap is a sequence, not a pick:** Mech Protocol (software beachhead) → safety
   co-processor on certified ASIL-D silicon (physical veto, zero tapeout) → "Mech Inside"
   certified module → fabless Mech-1 die → license the seal. Go fabless like ARM; let
   Thor/Qualcomm be the commodity muscle. Never pitch "out-NVIDIA NVIDIA on inference
   silicon" — that's the explicit trap.

## Naming (locked — don't reopen)

- Company: **Mechanical, Inc.** Brand: **Mechanical**. Shorthand: **Mech**.
- Chips: **Mech-1, Mech-2, …**  Software/control layer: **Mech Protocol.**  Cert: **the Mech seal.**
- Retired (don't reintroduce): Governor, Govern Protocol, Animae, Mecha, Mechanism, and the
  dozens of other rejected candidates. The engine-governor stays only as a *metaphor*.

## Open threads (state, so you don't re-litigate)

- **The proving ground lives in its own repo: `mechanicalsh/simulator`** (local checkout at
  `~/.superset/projects/simulator`). A Unitree G1 in Isaac Sim where the safety core will
  physically veto the robot's actuators. That demo *is* the thesis on camera before any
  silicon exists. De-contaminated from roboalias to syedos (identity + gist + token).
- **Rendering runs on Vast.ai (RTX 4090), not Modal.** The wall was Modal-specific: its GPU
  containers ship only the compute driver, so Isaac Sim's RTX renderer segfaults at NGX
  init. Vast rents the whole machine with the full graphics driver. Rule: A100/H100 have no
  RT cores — use RTX 4090 / L40 / A6000 for Isaac Sim. MuJoCo (G1 in Menagerie, runs locally
  on Apple Silicon) is a lighter alternative if you only need the veto logic.
- **Current state:** G1 renders live and streams to the browser; it settles under gravity
  (no controller yet). Next: a locomotion policy to stand/walk, then the veto layer.

## Domains

- **mechanical.sh** — platform front door (docs/app/api). **mech.la** — short link.

## Conventions

- Writing voice for any outward doc: plain, concrete, no jargon. The founder reacts hard to
  em-dashes, colons-as-drama, and "X, not Y" negation constructions — avoid them.
- When building any marketing site, default to **Mechanical UI** (the house design system at
  `~/mechanical-ui/`) unless told otherwise.
