---
doc_id: DRN-REQ-001
title: DustRunner requirements
project: DustRunner
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with a reference row and status against the concept
---

# DustRunner requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users or a pilot site, and will be checked by calculation at TRL 3. The status column compares them with the first-order estimates in DRN-PRC-001. Three requirements are **not met or not yet shown to be met** on paper: R14 (payback) is not met in the mid case, and R2 (cleaning effectiveness) and R3 (glass safety) cannot be shown without tests.

The **reference row** used throughout is one fixed-tilt table, one module high in portrait (1P), with 35 modules of 2,278 x 1,134 mm and about 580 W each: about 40 m long, about 90 m² of glass and about 20 kWp, tilted 25°, with the lower glass edge about 0.6 m above the ground.

| ID | Requirement | Target | Status (concept, estimate) | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Water-free cleaning | No water or liquid used in normal operation | Met by design | Design review |
| R2 | Cleaning effectiveness on dry dust | Daily dry pass keeps the average soiling loss at 1.5 % or less when the site soiling rate is 0.3 to 0.5 % per day | **Not shown**; depends on dust type and dew | Literature review at TRL 3; later soiling-station comparison |
| R3 | Glass and coating safety | Only microfiber touches the glass; brush interference 3 to 5 mm; no hard bristles, grit traps or metal within 10 mm of the glass; complies with the module maker's cleaning guidance | **Not shown**; abrasion over years is unknown | Maker guidance review; later abrasion test on sample glass |
| R4 | Fit the reference table | 1P portrait modules 2,278 mm long with 30 to 35 mm frames; short (top and bottom) edges free of clamps; tilt 10 to 35°; gaps between modules up to 25 mm; frame height steps up to 5 mm | Met on paper for the reference table; other module lengths need the beam and brush cut to length | Survey of target tables; model check |
| R5 | Coverage | 95 % or more of the glass area brushed per pass | About 98 % (2,198 of 2,228 mm of glass across the slope) | Model check |
| R6 | Rail-free installation | No rails along the row; only a dock at one end and clamp-on end stops at the other; no drilling of modules or structure; installed by two people in 60 min or less | Met by design; time unverified | Installation sequence review |
| R7 | Cycle time | A 100 m row cleaned out and back in 20 min or less | About 17 min at 0.2 m/s | Calculation |
| R8 | Energy autonomy | Three daily cycles on a 100 m row with no sun; recharged from the dock panel in one day at 3 peak sun hours | About 102 Wh usable against about 58 Wh for three cycles; about 45 Wh harvested at 3 sun hours against about 20 Wh per cycle | Energy calculation |
| R9 | Stay on the row | Two independent means stop the robot at each row end; hook rollers keep it on the table in operating wind; operation only below 8 m/s wind; robot parked and latched in the dock survives 35 m/s | End stops met by design; wind limits unverified | Wind load calculation; design review |
| R10 | Load on the modules | Robot mass 15 kg or less; each wheel load 60 N or less and carried on the frame only; no load on the glass except brush contact | About 12 kg; about 52 N per wheel with hook preload | Mass estimate; module maker's guidance |
| R11 | Environment | Electronics IP65; operates at 0 to 50 °C ambient on glass up to 75 °C; UV-stable plastics; dust-sealed bearings | By design; unverified | Datasheets and design review |
| R12 | Safe to be near | Emergency stop button on each end truck; brush and drives stop within 2 s of a stop command or of a truck lifting off the frame; brush ends guarded by the hood; nothing on the robot can reach PV cables, connectors or junction boxes | By design; unverified | Design review; later bench test |
| R13 | Affordable | Robot and dock, one row, $500 or less in parts | About $485 (indicative), thin margin | Priced BOM (`bom/bom.csv`) |
| R14 | Pays for itself | Value of the recovered energy covers the parts cost in 3 years or less on the reference row, mid case (0.3 % per day soiling, monthly manual wash as baseline, $0.10/kWh) | **Not met**: about 4 years in the mid case; about 2 years at 0.49 % per day or on a 100 m row | Energy yield calculation |
| R15 | Serviceable | Microfiber sleeve replaced in 15 min or less without taking the robot off the row; motors, bearings, wheels and battery are standard catalog parts | By design | Design review |

## Assumptions

- Specific yield about 5.5 kWh per kWp per day for a clean array at a sunny desert site (estimate).
- Soiling rate 0.3 % per day (mid case) and 0.49 % per day (high case, as measured at QEERI in Qatar; see DRN-PRB-001).
- Baseline practice is a manual wash every 30 days. Longer manual intervals, or no cleaning at all, make DustRunner's case stronger.
- Electricity or displaced diesel valued at $0.10/kWh. Diesel-displacing mini-grids are often higher.
- 20 W dock panel, 75 % derating for heat, dust, wiring and a simple charge controller.
- Wind and structural values are first-order and will be checked at TRL 3.
