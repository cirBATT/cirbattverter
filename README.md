# cirBATTverter 1 kW

An open hardware **48 V → 230 V sine-wave inverter**, designed to run from
second-life lithium battery packs.

Built by [cirBATT](https://cirbatt.com), Grenoble, France — we collect
end-of-life lithium batteries, requalify them cell by cell and reassemble them
into second-life packs. This inverter is the stage that turns such a pack into
usable mains power.

> ### ⚠️ This board handles lethal voltages
>
> The output is **230 V AC** and the DC bus is at **mains-level potential**.
> Capacitors stay charged after power-down. A lithium pack can deliver
> hundreds of amps into a short circuit.
>
> Do not build or power this board unless you are trained to work on mains
> equipment and have the right tools — isolation transformer, differential
> probes, RCD-protected bench. This design has **not** been certified to any
> safety standard. It is published as an engineering reference, not as a
> product ready to install in a home.

---

## Specifications

| | |
|---|---|
| Input voltage | 48 V nominal (lithium-ion pack) |
| Output voltage | 230 V AC |
| Output frequency | Set by the controller board |
| Rated power | 1 kW |
| Input stage | Semi-resonant DC-DC converter |
| Control | EGS005Q sine-wave driver board (off-the-shelf) |
| Copper weight | 70 µm on both boards |

The resonant frequency of the input stage is set on the controller board — see
[Getting started](#getting-started).

## What is in this repository

The project is made of **two boards**:

### `hardware/inverter/` — main board
KiCad 10 project. 4 copper layers, 1.6 mm, ~199 components. Includes the
custom symbol and footprint libraries it depends on (`Components_models/`,
`*.pretty/`) and STEP models in `3d/`.

### `hardware/planar-transformer/` — planar transformer
KiCad 10 project. 8 copper layers — the transformer windings are etched into
the PCB itself rather than wound on a bobbin, which keeps leakage inductance
low and the assembly flat and repeatable.

### `hardware/mechanical/`
`Cirbatt.step` — 3D model of the assembly, for enclosure design and fit checks.

### `production/`
Files to order the boards without opening KiCad:

| File | Use |
|---|---|
| `inverter/gerber.zip` | Gerbers for the main board |
| `inverter/*_JLCPCB_BOM.xlsx` | Bill of materials, JLCPCB format |
| `inverter/*_CPL_JLCPCB.xlsx` | Pick-and-place positions |
| `planar-transformer/Gerbers.zip` | Gerbers for the transformer |

> Specify **70 µm (2 oz) copper** when ordering. The default is 35 µm, and at
> 1 kW that difference matters: the tracks are sized for the heavier copper.

## Getting started

**1. Open the design.** Install [KiCad 10](https://www.kicad.org/download/) or
later and open `hardware/inverter/cirBATTverter_1KWH.kicad_pro`. The custom
libraries are referenced relatively, so they resolve as long as you keep the
folder structure.

**2. Order the boards.** Upload the files from `production/` to your
fabricator. Both boards need 70 µm copper.

**3. Get the controller.** The SPWM control is **not** on this board. It uses
an **EGS005Q** driver module, a widely available off-the-shelf part. Its user
manual and schematic are published by the manufacturer — we do not redistribute
them here, as they are not ours to license. Search for *EGS005Q sine wave
inverter driver board* to find the current documentation and suppliers.

**4. Set the resonant frequency** of the input stage on the controller board,
to match the semi-resonant converter.

## Licence

Hardware is released under the
**[CERN Open Hardware Licence Version 2 — Strongly Reciprocal](LICENSE)**
(`CERN-OHL-S-2.0`).

In short: you may study, modify, manufacture and sell this design, including
commercially. If you distribute a modified version, or a product containing
one, you must make your modified sources available under the same licence.
Improvements to the design stay available to everyone.

This is a reciprocal licence by choice. We would rather the design stay open
than be absorbed into a closed product.

## Contributing

Issues and pull requests are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
Bench measurements, thermal data and failure reports are especially useful: we
publish the design, but real-world validation is what makes it trustworthy.

## Contact

[cirbatt.com](https://cirbatt.com) · contact@cirbatt.com
