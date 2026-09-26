---
doc_id: DRN-REQ-001
title: DustRunner requirements
project: DustRunner
doc_type: Requirements
version: "0.4"
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply DRN-DDR-001 (R14 restated for rows of 60 m or more; R13 covers the anemometer; reference row and table format kept); status from DRN-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). R9 restated with a 6 m/s start limit and 8 m/s abort limit; R10 allows 75 N for the row-entry transient; status from DRN-CAL-001 v0.2
---

# DustRunner requirements

These requirements are checked by calculation in DRN-CAL-001 v0.2. On paper, seven are met, four are at risk and four cannot be verified at TRL 3; none is clearly not met. The four at risk are R4 (5 mm frame steps and frame flange width), R9 (traction in wind along the row, margin 1.33 at the 6 m/s start limit but 1.00 if friction is only 0.3), R11 (pack temperature while charging in the sun) and R13 (the priced BOM is exactly $500). R10 is now met after DRN-DDR-002 allowed 75 N for the brief row-entry transient. R2, R3, R6 and R15 need tests or trials. Targets are still proposals for review, not validated with users or a pilot site, except where DRN-DDR-001 or DRN-DDR-002 records Amish's decision.

The **reference row** used throughout, kept by DRN-DDR-001 (D7), is one fixed-tilt table, one module high in portrait (1P), with 35 modules of 2,278 x 1,134 mm and about 580 W each: about 40 m long, about 90 m² of glass and about 20 kWp, tilted 25°, with the lower glass edge about 0.6 m above the ground. The first supported table format is 1P portrait with 2,278 mm modules (DRN-DDR-001, D10).

*Table 1. Requirements and status at TRL 3.*

| ID | Requirement | Target | Status (DRN-CAL-001) | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Water-free cleaning | No water or liquid used in normal operation | Met by design | Design review |
| R2 | Cleaning effectiveness on dry dust | Daily dry pass keeps the average soiling loss at 1.5 % or less when the site soiling rate is 0.3 to 0.5 % per day | **Not verifiable at TRL 3**; depends on dust type and dew. R14 on the 60 m row holds while the residual stays below 1.7 % | Later soiling-station comparison |
| R3 | Glass and coating safety | Only microfiber touches the glass; brush interference 3 to 5 mm along the whole brush; no hard bristles, grit traps or metal within 10 mm of the glass; complies with the module maker's cleaning guidance | **Not verifiable at TRL 3**; geometry met (3.4 to 4.4 mm with a 50 mm core; nothing else within 10 mm); abrasion over years unknown | Maker guidance review; later abrasion test on sample glass |
| R4 | Fit the reference table | 1P portrait modules 2,278 mm long with 30 to 35 mm frames; short (top and bottom) edges free of clamps; tilt 10 to 35°; gaps between modules up to 25 mm; frame height steps up to 5 mm | **At risk**: 25 mm gaps pass; a 5 mm step needs about 9 N against about 14 N spare traction; the wheel tread needs a visible frame flange of about 21 mm or more | Survey of target tables and frame profiles |
| R5 | Coverage | 95 % or more of the glass area brushed per pass | Met: 98.4 % on the 40 m row | Model check |
| R6 | Rail-free installation | No rails along the row; only a dock at one end and clamp-on end stops at the other; no drilling of modules or structure; installed by two people in 60 min or less | **Not verifiable at TRL 3**; rail-free and clamp-on by design; time unverified | Installation trial |
| R7 | Cycle time | A 100 m row cleaned out and back in 20 min or less | Met: 17.4 min | Calculation |
| R8 | Energy autonomy | Three daily cycles on a 100 m row with no sun; recharged from the dock panel in one day at 3 peak sun hours | Met: 67 of 102 Wh usable; 45 Wh harvested against 23 Wh a day | Energy calculation |
| R9 | Stay on the row | Two independent means stop the robot at each row end; hook rollers keep it on the table in operating wind; a run starts only when the dock anemometer reads below 6 m/s and aborts to the dock above 8 m/s (DRN-DDR-002, N1); robot parked and latched in the dock survives 35 m/s | **At risk**: parked, latch and end stops hold with factors over 4; traction margin 1.33 at the 6 m/s start limit and 1.10 at the 8 m/s abort limit at friction 0.4, but 1.00 and 0.82 at friction 0.3 | Wind load calculation; later friction measurement |
| R10 | Load on the modules | Robot mass 15 kg or less; each wheel load 60 N or less in steady running and 75 N or less for the brief transient as the lead wheels enter the first module (DRN-DDR-002, N2), subject to the module maker's frame loading guidance; carried on the frame only; no load on the glass except brush contact | Met on paper: 13.8 kg; 58 N per wheel brushing at worst tilt; about 72 N for about a second at row entry | Mass estimate; module maker's guidance |
| R11 | Environment | Electronics IP65; operates at 0 to 50 °C ambient on glass up to 75 °C; UV-stable plastics; dust-sealed bearings | **At risk**: the parked pack may exceed its 45 °C charging limit in the sun; a sunshade is added | Datasheets and design review; later thermal check |
| R12 | Safe to be near | Emergency stop button on each end truck; brush and drives stop within 2 s of a stop command or of a truck lifting off the frame; brush ends guarded by the hood; nothing on the robot can reach PV cables, connectors or junction boxes | Met on paper: brush stops in 0.13 s, robot in 0.06 s; guards by design | Design review; later bench test |
| R13 | Affordable | Robot, dock and anemometer for one row, $500 or less in parts (`budget_usd`) | **At risk**: $500.00 indicative, no margin; budget kept at $500 and revisited when quotes exist (DRN-DDR-002, N3) | Priced BOM (`bom/bom.csv`) |
| R14 | Pays for itself | Value of the recovered energy covers the parts cost in 3 years or less on rows of 60 m or more, mid case (0.3 % per day soiling, monthly manual wash as baseline, $0.10/kWh) | Met: 2.8 years on a 60 m row; 1.6 years on a 100 m row (4.1 years on the 40 m reference row, which is below the scope of R14) | Energy yield calculation |
| R15 | Serviceable | Microfiber sleeve replaced in 15 min or less without taking the robot off the row; motors, bearings, wheels and battery are standard catalog parts | **Not verifiable at TRL 3**; catalog parts by design | Later service trial |

## Assumptions

- Specific yield about 5.5 kWh per kWp per day for a clean array at a sunny desert site (estimate).
- Soiling rate 0.3 % per day (mid case) and 0.49 % per day (high case, as measured at QEERI in Qatar; see DRN-PRB-001).
- Baseline practice is a manual wash every 30 days. Longer manual intervals, or no cleaning at all, make DustRunner's case stronger.
- Electricity or displaced diesel valued at $0.10/kWh. Diesel-displacing mini-grids are often higher.
- 20 W dock panel, 75 % derating for heat, dust, wiring and a simple charge controller.
- Friction coefficients, brush pile pressure and the visible frame flange width are assumptions listed in DRN-CAL-001, Table 1, and must be measured.
