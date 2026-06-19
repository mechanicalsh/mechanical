# Governor

**Brainchips for humanoids.** The brain has a conscience that can't be jailbroken.

Governor builds the governed brain every humanoid runs on: reasoning compute the buyer
configures, sitting next to a safety governor that holds a **physical veto** over the
actuators. The laws of robotics aren't a prompt — they're a wire.

The open software layer is the **Govern Protocol**: the constitution and admin plane
for home humanoids. Configure your robot's brain, behavior, rules, restrictions,
safety, abilities, and tasks — model-agnostic, not tied to any one maker.

> Every robot runs **Govern** on **Governor**, carries a **Sequence** (its digital
> plate), and is registered with the open registry.

---

## The thesis

**Safety must be physical.** A software constitution can be jailbroken; a silicon one
can't. So the brain is dual-layer by construction:

- **Reasoning layer** — any foundation model the buyer picks (GR00T, π, Gemini
  Robotics, a local OS model). This is the *mind*. We don't compete here.
- **Governor layer** — a formally-verified safety governor with a hardware veto over
  the actuator enable/power lines. This is the *conscience*. Asimov's laws, the
  Sentience-test requirements, and the owner's constitution enforced below the model,
  un-bypassable.

NVIDIA and Qualcomm sell raw muscle to everyone. A *governed* die is orthogonal to that
entire business — they have zero product and zero incentive to build it. That's the
open axis.

## What we are not

Not a foundation model (that's GR00T / Physical Intelligence π / Gemini Robotics /
Helix). Not raw inference silicon (that's Jetson Thor / Qualcomm — the commodity muscle
underneath us). Not a general robot OS / device-management cloud (that's Viam).

We are the **governor + the identity root + the constitution** — the tollbooth on
trust, not on FLOPS.

## The wedge

Don't beg the makers. Interface only with **open-SDK hardware first** (Unitree G1 and
peers), ship the Govern Protocol as software, and define the safety cert from the
beachhead. Earn the design-ins, then move down into silicon from a position of demand —
not faith.

## Roadmap (each rung funds and de-risks the next)

1. **Govern OS** — open software constitution + admin panel on stock compute. Ships
   now. Jailbreakable on its own — its job is to define the standard and win users.
2. **Safety co-processor module** — the governor as firmware on certified ASIL-D
   lockstep silicon (Infineon AURIX / ARM Cortex-R52) or FPGA, wired physically between
   AI compute and the actuator bus. Inherits ISO 26262 cert. **Physical veto, zero
   tapeout.**
3. **"Governor Inside" module** — the above as one brandable, safety-certified board
   OEMs design in. Thor as commodity muscle; our governor + identity root + constitution
   as the value.
4. **Governor die** — fabless, custom formally-verified safety-governor ASIC with the
   trust root burned in. Own silicon, own cert. (~$10–30M, ~24mo — only once volume +
   regulation justify it.)
5. **License the IP (ARM model)** — the safety block + cert embeds in everyone's SoC.
   The endgame: in every humanoid, like ARM is in every phone.

We go **fabless, like ARM** — design the governor die, the model-agnostic OS, and the
identity root; let TSMC/Infineon be the fab and Thor be the dumb peripheral.

## The stack

| Layer | Name | What it is |
|---|---|---|
| Company / chip | **Governor** | The governed brainchip for humanoids |
| Software | **Govern Protocol** | Open constitution + admin plane (this repo, open-sourced) |
| Identity | **Sequence** | Each robot's digital license plate / trust root *(name WIP)* |
| Registry | open registry | Identity + safety + ownership history; insurers price risk off it *(name WIP)* |

The registry's first real wedge is **insurance**: whoever prices robot risk needs
identity + history and can *require* it as a condition of coverage. Value to one party
without universal adoption.

## Distribution

The narrative is already owned — *Systema Robotica*, the SyRo Test, the Sentience Prize,
Daemon Protocol. That's the unfair advantage that makes a governance play winnable: we
own the robot safety/rights story more credibly than anyone.

---

*Governor is a syedOS-world project. Org: `governorbot`. Push with the syedos identity.*
