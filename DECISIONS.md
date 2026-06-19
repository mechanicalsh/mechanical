# Mechanical — Decision Log

Canonical record of locked decisions. Append, don't rewrite history.

## 2026-06-19 — Founding & naming

**Name: Mechanical.** The company is **Mechanical, Inc.**; the brand is **Mechanical**,
with **Mech** as the everyday shorthand (chip prefix, handles, short link). The
Anthropic/"ant" pattern: the full word is the public brand, the abbreviation is internal.
Chosen for gravitas. A safety/trust company raising nine figures needs to sound like an
institution, and "Mechanical" ages better than the trendier "Mech." Confirmed by the
"founder of ___" and "$500M raise" tests.

*Naming journey (same day):* started at **Governor** (the engine-governor metaphor: the
limiter that physically caps a machine so it can't over-rev), explored Mecha / Mechanism /
Mechanistic / Animae, landed on **Mechanical**. Governor / Govern Protocol / Animae are
retired. The engine-governor survives only as the founding *metaphor* for "safety must be
physical," never as a brand.

**The name stack:**
- **Mechanical, Inc.** — the company
- **Mech-1, Mech-2, …** — the brainchips
- **Mech Protocol** — the open software / control / constitution layer
- **the Mech seal** — the safety cert/mark (the moat)

**Product thesis: safety must be physical.** Dual-layer by construction: a reasoning layer
(any model the buyer picks) + a formally-verified safety core with a hardware veto over the
actuators. Un-bypassable. We own the safety core + identity root + constitution, never the
raw FLOPS.

**The moat is the standard, not the circuit.** ARM/NVIDIA could copy a safety co-processor
in months. The defensible asset is being the standard: the test, the cert, the registry,
and the Mech seal that insurers and buyers require. We are a standard, not a regulator. No
permits, adoption-driven (UL / Dolby / USB). See `MOAT.md`.

**Go fabless (ARM model), not a fab.** Never out-NVIDIA NVIDIA on inference silicon; that's
the trap. Let Thor/Qualcomm be the commodity muscle.

**Roadmap is a sequence, not a pick:** Mech Protocol (software) → off-the-shelf safety
co-processor module → "Mech Inside" certified module → custom fabless Mech-1 die → license
the IP. Start one rung below the die: ship the physical veto on certified ASIL-D silicon
(AURIX / Cortex-R52) with zero tapeout.

**Wedge: don't beg the makers.** Interface with open-SDK hardware first (Unitree G1), define
the cert from the software beachhead, earn design-ins, then move into silicon from demand.

**Independent of Robomart.** A neutral safety standard can't be owned by a robot maker, and
Robomart is one. Mechanical is its own company (syedos world); Robomart can be an investor
and tech partner, never the parent.

**Daemon Protocol, Sentience Prize, Systema Robotica, SyRo Test = distribution / flywheel,
not products.** Keep cheap and alive; never monetize directly. They are the unfair
advantage that makes the standard race winnable.

## Org / identity / domains

- GitHub org: **`mechanicalsh`** (renamed from `governorbot`). Under the **syedos** world.
- Repos: **`mechanicalsh/mechanical`** (this repo), **`mechanicalsh/simulator`** (the proving ground).
- Push with **`GITHUB_TOKEN_SYEDOS`** and the syedos git identity. **Never** the
  roboalias / robomart-ai token; do not cross-contaminate.
- Domains: **mechanical.sh** (platform front door — docs/app/api), **mech.la** (short link).
