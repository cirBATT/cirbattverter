# Contributing to cirBATTverter

Thanks for looking. This is a working engineering design, not a finished
product, so there is plenty to improve.

## What helps most

**Bench data.** We publish the design; what it needs is independent
validation. Efficiency curves, thermal images under load, waveforms at the
switching nodes, behaviour at the limits — all of it is more valuable than
another layout tweak. Open an issue with your measurements, your setup and
the conditions.

**Failure reports.** If something blew up, we want to know what and why.
Include the conditions, what you measured and, where you can, photographs.
A documented failure is worth more to the next builder than a clean build.

**Build reports.** Tell us it worked, with which fabricator, which copper
weight and which component substitutions. That turns a schematic into
something others can trust.

**Design issues.** Creepage and clearance, derating, EMC, protection
coverage. Point at the specific net or component and say what you would
change.

## Working on the files

The project is KiCad 10. Open
`hardware/inverter/cirBATTverter_1KWH.kicad_pro` — the custom libraries are
referenced relatively and resolve from the repository layout, so keep the
folder structure as it is.

A few practical points:

- **Do not commit `.kicad_prl` files or backups.** They are per-user state and
  are already ignored.
- **KiCad files are text, but they do not merge well.** Say in your issue or
  pull request what you are changing before you start on the PCB, so two
  people do not rework the same area.
- **If you change the layout, regenerate the files in `production/`** —
  Gerbers, BOM and CPL — so they stay consistent with the design.
- **Keep the 70 µm copper assumption** unless you resize the tracks for
  something else, and say so explicitly if you do.

## Pull requests

Describe what changed and why, and what you did to verify it. For a hardware
change, "verified" means measured or at least simulated — not "it should
work". If you could not test it, say so; an untested but well-argued change is
still welcome, it just gets reviewed differently.

## Licence

The hardware is under
[CERN-OHL-S-2.0](LICENSE), a strongly reciprocal licence. By contributing you
agree that your contribution is licensed the same way, so that it stays
available to everyone downstream.

## Safety

Please do not post build instructions or encouragement that skip the safety
basics. This board produces 230 V AC and runs from a battery that can deliver
enormous fault currents. Anyone reproducing it should be equipped to work on
mains, and the documentation should keep saying so.
