# DustRunner

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** CleanTech · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $500 USD · **Difficulty:** 4 of 5

Rail-free crawler robot that uses a rotating microfiber brush to dry-clean panel rows, clamps onto panel edges and docks to recharge.

![DustRunner concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

Soiling cuts output of PV arrays in dusty regions by 15 to 25%, and water for washing is scarce.

## Concept

Rail-free crawler robot that uses a rotating microfiber brush to dry-clean panel rows, clamps onto panel edges and docks to recharge.

The robot spans one table from its lower to its upper module edge. End trucks ride on the module frames and hook under the frame lips, so no rails are needed along the row. A 2.2 m microfiber brush sweeps the glass dry once a day, and the robot parks off the glass in a clamp-on dock where a 20 W panel recharges its 12.8 V LiFePO4 pack. First-order estimates for a 40 m, 20 kWp row: about 7 minutes and 8 Wh per cycle, about 12 kg, and about $485 in parts for robot and dock. These are concept estimates, not test results.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Microfiber brush, 120 mm x 2.2 m, with brush motor and hood
- End trucks with belt-linked wheels and two drive gearmotors
- Edge-guide and hook rollers (the rail-free "clamp")
- 12.8 V 10 Ah LiFePO4 pack
- Controller (ESP32 class) and IR edge sensors
- Clamp-on dock with a 20 W PV panel and charger; clamp-on end stops

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (DRN-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `DRN-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
