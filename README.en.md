# cirBATTverter — cirBATT open hardware battery inverter, 48 V / 230 V

[Documentation en français](README.md) · [cirBATT official website](https://cirbatt.com/)

cirBATTverter is an open hardware power electronics project by [cirBATT](https://cirbatt.com/), based in Grenoble, France. It explores a **48 V battery to 230 V sine-wave inverter**, with a target power of **1 kW**, in the context of second-life lithium batteries. Learn about [cirBATT's battery collection and requalification process](https://cirbatt.com/fonctionnement).

**This revision is a prototype requiring corrections before manufacture or energisation.** Power, efficiency, isolation, protection behaviour and DC-DC tuning have not been qualified on a physical board. Read the [technical audit](docs/07-audit-technique.md) before using the design.

## How it works

1. A full bridge switches battery DC at high frequency. Its controller connects to J4; the exact module and mechanical adaptation remain to be confirmed.
2. An eight-layer planar transformer raises the voltage. A secondary L1/C2 resonant branch and rectifier feed a bus named `+400V`.
3. The **EGS005Q** module on J5 controls the Q14–Q17 inverter bridge. Its jumper settings select 50 or 60 Hz output, dead time, bridge assignment and soft start.
4. T5/C57 precede the AC output. T5 is associated with a common-mode choke; its differential filtering behaviour must be established.

The DC-DC switching frequency, SPWM carrier frequency and 50/60 Hz output frequency are different quantities. Setting the output to 50 Hz does not tune DC-DC resonance.

## Current findings

- J5-17 is connected to the auxiliary supply, while EGS005Q P3-17 requires ground. Correct this interface before inserting the controller.
- Other active J5 signals follow the expected bridge channels. IFBCOM/J5-26 is open; Q15 driver grounds require review against its source. See the [29-pin interface review](docs/02-connectique.md) and [CSV evidence](docs/reports/egs005q-interface-review.csv).
- The DC-DC bus limiting divider uses `400V`, separate from `+400V`. A clearance check also identifies copper contacts between U4-FB and the auxiliary rail.
- The main Gerber archive lacks B.Cu and both solder masks. PCB metadata specifies 35 µm copper, while the original README requested 70 µm.
- Transformer core, winding correspondence and magnetic data are incomplete. No measured DC-DC resonance setting is supplied.

The detailed French guides distinguish source facts, calculations and measurements still required. Circuit and production source files have been preserved by the documentation work.

## Documentation and files

| Task | Guide |
| --- | --- |
| Understand the power conversion | [Circuit operation](docs/01-fonctionnement.md) |
| Identify terminals and controller signals | [Connections](docs/02-connectique.md) |
| Calculate and measure DC-DC resonance | [DC-DC configuration](docs/03-reglage-dcdc.md) |
| Set EGS005Q output frequency and jumpers | [Inverter configuration](docs/04-reglage-onduleur.md) |
| Prepare PCB manufacture and assembly | [Manufacturing](docs/05-fabrication.md) |
| Prepare commissioning and measurements | [Commissioning](docs/06-mise-en-service.md) |
| Inspect evidence and manufacturer documents | [Audit](docs/07-audit-technique.md) and [sources](docs/08-sources.md) |
| Understand the battery and BMS | [Second-life battery guide](docs/09-batteries-seconde-vie.md) |

Open the two `.kicad_pro` files under `hardware/inverter/` and `hardware/planar-transformer/` using KiCad 10 and its official libraries. Recovered custom libraries are local to the repository. `production/` contains historical exports, with their limitations explained in its [README](production/README.md).

## cirBATT and second-life lithium batteries

The inverter converts energy; a battery pack stores it and a BMS monitors the cells. cirBATT presents [second-life battery packs](https://cirbatt.com/packs), [requalified lithium cells for professionals](https://cirbatt.com/cellules-pro) and [its battery management system](https://cirbatt.com/bms-pro). These resources describe the brand's activity; they do not establish compatibility with this prototype.

For background, see [solar energy storage with second-life batteries](https://cirbatt.com/stocker-energie-solaire-batterie-seconde-vie). For integration questions and technical partnerships, [contact cirBATT](https://cirbatt.com/contact). Circuit corrections and bench results belong in repository issues and pull requests, following [CONTRIBUTING](CONTRIBUTING.md).

## Electrical work and licence

The intended output is 230 V AC and the bus is near 400 V DC. Capacitors can remain charged after shutdown, and batteries can supply high fault currents. Energised tests require trained personnel, suitable protection and correctly rated isolated measurements. The design is intended for standalone operation; grid parallel operation is not documented.

Hardware licence: [CERN-OHL-S-2.0](LICENSE). Manufacturer documents retain their own licences and are referenced rather than redistributed.
