# Mechanical

**Brainchips for humanoids. The brain has a conscience that can't be jailbroken.**

Mechanical builds the governed brain every humanoid runs on: reasoning compute the buyer
configures, sitting next to a safety core that holds a **physical veto** over the
actuators. The laws of robotics aren't a prompt, they're a wire.

The open software layer is the **Mech Protocol**: the constitution and admin plane for
home humanoids. Configure your robot's brain, behavior, rules, restrictions, safety,
abilities, and tasks. Model-agnostic, never tied to one maker.

> Every robot runs the **Mech Protocol** on a **Mech** chip, certified to the **Mech**
> safety standard.

---

## The thesis

**Safety must be physical.** A software constitution can be jailbroken; a silicon one
can't. So the brain is dual-layer by construction:

- **Reasoning layer** — any foundation model the buyer picks (GR00T, π, Gemini Robotics,
  a local OS model). This is the *mind*. We don't compete here.
- **Safety core** — a formally-verified safety governor with a hardware veto over the
  actuator enable/power lines. This is the *conscience*. Asimov's laws, the Sentience-test
  requirements, and the owner's constitution enforced below the model, un-bypassable.

NVIDIA and Qualcomm sell raw muscle to everyone. A governed die is orthogonal to their
whole business; they have zero product and zero incentive to build it. That's the open
axis.

## What we are not

Not a foundation model (that's GR00T, Physical Intelligence π, Gemini Robotics, Helix).
Not raw inference silicon (that's Jetson Thor and Qualcomm, the commodity muscle
underneath us). Not a general robot OS or device-management cloud (that's Viam).

We are the **safety core, the identity root, and the constitution**: the tollbooth on
trust, not on FLOPS.

## The wedge

Don't beg the makers. Interface only with **open-SDK hardware first** (Unitree G1 and
peers), ship the Mech Protocol as software, and define the safety cert from the beachhead.
Earn the design-ins, then move down into silicon from a position of demand, not faith.

## Roadmap (each rung funds and de-risks the next)

1. **Mech Protocol (software)** — open constitution + admin panel on stock compute. Ships
   now. Jailbreakable on its own; its job is to define the standard and win users.
2. **Safety co-processor module** — the safety core as firmware on certified ASIL-D
   lockstep silicon (Infineon AURIX, ARM Cortex-R52) or FPGA, wired physically between AI
   compute and the actuator bus. Inherits ISO 26262 cert. **Physical veto, zero tapeout.**
3. **"Mech Inside" module** — the above as one brandable, safety-certified board OEMs
   design in. Thor as commodity muscle; our safety core, identity root, and constitution
   as the value.
4. **Mech-1 die** — fabless, custom formally-verified safety-governor ASIC with the trust
   root burned in. Own silicon, own cert. (~$10–30M, ~24mo, only once volume + regulation
   justify it.)
5. **License the IP (ARM model)** — the safety block + cert embeds in everyone's SoC. The
   endgame: in every humanoid, like ARM is in every phone.

We go **fabless, like ARM**: design the Mech die, the model-agnostic protocol, and the
identity root; let TSMC/Infineon be the fab and Thor be the dumb peripheral.

## The stack

| Layer | Name | What it is |
|---|---|---|
| Company | **Mechanical, Inc.** | Brainchips + the safety standard for humanoids |
| Chips | **Mech-1, Mech-2, …** | The governed brainchips (safety core on die) |
| Software | **Mech Protocol** | Open constitution + admin plane (open-sourced) |
| Standard | **the Mech seal** | The cert/mark insurers and buyers require |

The standard's first real wedge is **insurance**: whoever prices robot risk needs identity
and history, and can *require* the Mech seal as a condition of coverage. Value to one party
without universal adoption.

## Distribution

The narrative is already owned: *Systema Robotica*, the SyRo Test, the Sentience Prize.
That's the unfair advantage that makes a safety-standard play winnable. We own the robot
safety/rights story more credibly than anyone.

---

*Mechanical is a syedOS-world project. Org: `mechanicalsh`. Repo: `mechanicalsh/mechanical`.
Push with the syedos identity. Brand: **Mechanical** (full word); **Mech** is the
shorthand for the chip line and handles. Domains: **mechanical.sh** (platform front door),
**mech.la** (short link).*
