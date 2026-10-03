---
doc_id: DRN-CAL-001
title: DustRunner sizing calculations
project: DustRunner
doc_type: Calculation
version: "0.6"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (mass, brush contact and deflection, wheel loads and traction, wind, beam, energy, coverage, stopping, cost and payback)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Traction margin at the 6 m/s start limit added [C13]; R9 and R10 checked against the restated targets of DRN-REQ-001 v0.4
- version: "0.3"
  date: '2026-09-30'
  author: Amish Chadha
  change: Re-run for the constructable design (DRN-DDR-003). Fittings added for construction [A4]; hook preload set by the 60 N rule [C0]; payback row length [I9]; R10 and R14 now not met, R13 over the value-engineering target
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Requirement status updated for Amish''s decisions of 2026-10-02: R10 mass limit restated as 16.5 kg (met on paper), R14 kept and at risk; no number re-run'
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Script re-run with R10 restated to 16.5 kg and R14 marked at risk, so the printed counts [J0] agree with the decided counts; cost wording in [I1] changed to the value-engineering wording; no computed number changed'
---

# DustRunner sizing calculations

On paper, DustRunner meets six of its fifteen requirements, has four at risk and one short of its target; four cannot be verified at TRL 3 (status as decided by Amish on 2026-10-02, below). Version 0.3 re-runs every number for the constructable design of DRN-DDR-003, which adds the bearings, housings, brackets, clamps and fittings that the concept left out. Those parts add about 2.1 kg and $73, and that is what moves three requirements off their targets: the robot weighs 15.9 kg against the 15 kg of R10 (although every wheel load still meets R10's 60 N steady and 75 N transient limits, because the hook preload drops from 70 N to 60 N by the same rule that set it); the parts cost $573, USD 73 over the $500 value-engineering target of R13; and the payback on a 60 m row is 3.2 years against the 3 years of R14 (it is met on rows of 63.5 m or more). The three at risk are frame fit (R4), where a 5 mm height step between modules is climbable only with both wheels driven and a thin margin; staying on the row (R9), where traction at the 6 m/s start limit set by DRN-DDR-002 is 1.30 times the resistance at an assumed friction coefficient of 0.4, but only 0.98 at 0.3; and environment (R11), where the pack may exceed its 45 °C charging limit in the sun. On 2026-10-02 Amish restated R10's mass limit as 16.5 kg, keeping the wheel-load limits, so R10 is met on paper and the robot is weighed at TRL 4, and kept R14 at 3 years on rows of 60 m or more, marked at risk until quotes; the mass and cost savings worth trying are in DRN-DEC-001. The TRL 3 calculations had already changed three parts of the TRL 2 concept: the brush core grew from 40 mm to 50 mm so that the pile interference stays in the 3 to 5 mm band along the whole brush, the hook preload was set by a wheel-load rule, and the hood is thinner (0.8 mm). Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [C4], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not replace tests of traction, wind hold-down, end stops, stopping time, battery temperature or glass abrasion, and nothing may be installed on a live array on the strength of this note. See DRN-PRC-001, Safety.

## Scope and method

The note checks every requirement in DRN-REQ-001 v0.5 against the design in DRN-PRC-001 v0.5 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `derived()` and part solids, so the beam, brush, hood, trucks, wheels, rollers, enclosures and the fittings added for construction used here are the ones in the STEP files, in drawing DRN-DWG-001 and in the build plan DRN-BLD-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is the reference row of DRN-REQ-001: a 1P portrait table of 2,278 x 1,134 mm modules at 25° tilt, 35 modules long (40.4 m, 20.3 kWp). The robot travels at 0.2 m/s out and back, brushing both ways. Longer rows of 52 modules (60.0 m) and 87 modules (100.4 m) are used for R7, R8 and R14.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Masses | Aluminum 2,700 kg/m³ for the beam, core, hood, plates, housings, brackets and cleats from the model; microfiber pile 40 kg/m³ over its annulus; bought parts from typical catalog values (Table 2) | To confirm by weighing parts |
| Brush contact | Mean pile pressure 750 Pa at 4 mm interference (range 500 to 1,000 Pa), treated as a linear spring; friction of microfiber on dry dusty glass 0.45 (range 0.3 to 0.6); 150 rpm | Assumed; the largest uncertainty in the power budget. To measure |
| Traction | Polyurethane on dusty anodized aluminum, friction 0.4 (range 0.3 to 0.6); rolling coefficient 0.02 for wheels and rollers; along-row grade 2° | Assumed; to measure on real frames |
| Frame | Top flange 25 mm wide, frame 33 mm deep, top 1 mm proud of the glass | Assumed from the reference module; not from a datasheet |
| Wind | Start limit 6 m/s and abort limit 8 m/s along the row at the dock anemometer (DRN-DDR-002); air 1.2 kg/m³; side drag coefficient 1.5 on the robot's along-row silhouette; lift coefficient 1.0 on its plan area; normal-force coefficient 1.2 on the dock panel | Bluff-body handbook ranges, conservative |
| Electrical | Brush drive 60 % efficient, wheel drives 50 %, electronics 3 W running and 0.15 W standby; charging and pack 96 %; 128 Wh pack, 80 % usable | Typical small gearmotors and LiFePO4 packs |
| Charging | 20 W panel derated to 75 %; 3 sun hours design day, 5.5 typical | DRN-REQ-001 |
| Yield and value | 5.5 kWh per kWp per day; 0.58 kWp per module; soiling 0.3 %/day (mid) or 0.49 %/day (high); monthly manual wash as the baseline, so its average loss is half the loss at 30 days; 1.5 % residual loss with daily cleaning (R2, unverified); $0.10/kWh | DRN-REQ-001 and DRN-PRB-001 |
| Hardware | 6 mm latch pin, 100 MPa allowable shear; clamp bolts preloaded to 5 kN with friction 0.3; 5 mm rubber buffer on the end stops | Typical values; to confirm at detail design |

*Table 2. Bought-part masses used [A2].*

| Part | Mass (kg) |
| --- | --- |
| Brush gearmotor and belt drive | 0.80 |
| Two drive gearmotors | 0.50 |
| Guide and hook rollers | 0.35 |
| LiFePO4 pack | 1.30 |
| Controller in its IP65 box | 0.45 |
| Four IR sensors | 0.12 |
| Wiring, fuse, main switch and cable ties | 0.50 |
| Per truck: four 10 mm flange bearings, axles, pulleys, belt and coupling | 0.30 |
| Two 20 mm brush flange bearings | 0.40 |
| Two stop buttons, latch solenoid, pack straps, cleat and hood screws | 0.34 |

## A. Mass and balance (R10)

The robot weighs about 15.9 kg [A3], against the 16.5 kg of R10 (restated from 15 kg on 2026-10-02), 13.8 kg in version 0.2 and about 12 kg at TRL 2. The made parts from the model are the beam (2.92 kg), the brush with its 50 mm core, end plugs and flange bearings (3.54 kg), the hood and sunshade (1.06 kg) and the two trucks with wheels, drive housings and bearings (3.64 kg) [A1]. The parts added to make the design buildable weigh about 2.1 kg in all (2.08 kg): drive housings, roller clevises, hook sliders, brackets, cleats, sunshade posts and core plugs 1.17 kg; brush flange bearings 0.40 kg; stop buttons, latch solenoid, straps and screws 0.34 kg; and 0.17 kg from truck plates 24 mm taller to carry the hook spring [A4]. R10's mass limit is therefore not met. The center of mass is 959 mm up the 2,278 mm slope, because the pack and controller sit near the lower end, and 116 mm above the glass [A3].

## B. Brush contact, drag and deflection (R3, R8)

The TRL 2 figure of about 30 W of brush drag holds. Treating the pile as a spring of about 8.1 kN/m per meter of brush, the brush presses on the glass with about 67 N, the tangential drag is about 30 N at 0.94 m/s surface speed, and the brush needs about 29 W mechanical and 48 W electrical [B1]. Over the assumed ranges of pile pressure and friction the mechanical power runs from 13 W to 51 W [B2, B3], so this is the first number to measure.

The core tube bends under the pile reaction. Modeled as a pinned tube between the truck bearings on an elastic foundation, a 40 x 2 mm core lets the interference fall to 2.9 mm at mid-span [B4], below the 3 mm lower limit of R3. A 50 x 2 mm core with 4.5 mm nominal interference at the bearings keeps it at 3.5 to 4.4 mm along the whole brush [B5]. The model and BOM now use the 50 mm core.

The model has no solid other than the brush sleeve within 10 mm of the glass: the core tube is 30 mm and the hood edges 80 mm above the glass [B6]. The geometric part of R3 is therefore met; abrasion of the coating over years cannot be calculated.

## C. Wheel loads, traction and frame steps (R4, R9, R10)

The hook preload is set by one rule: the highest value, in 5 N steps, that keeps the steady brushing wheel load at 60 N or less at every tilt from 10° to 35°. With the heavier constructable robot the rule gives 60 N per truck (worst steady wheel load 58.6 N; 65 N would give 61.1 N) [C0], down from 70 N in version 0.2. The extra weight and the lower preload nearly cancel, so the wheel loads and the traction barely change.

*Table 3. Wheel loads at 25° tilt with 60 N hook preload per truck.*

| Case | Lower wheels (each) | Upper wheels (each) | Tag |
| --- | --- | --- | --- |
| Brushing on the row | 56 N | 41 N | [C1] |
| Brush off the glass (parked, or lead wheel entering the first module) | 73 N | 58 N | [C2] |
| Brushing at 10° tilt | 59 N | 45 N | [C8] |
| Brushing at 35° tilt | 53 N | 37 N | [C9] |

The brush reaction lifts the robot off the frames by about 67 N, so the wheel loads while brushing are lower than when the brush is off the glass. The only time a wheel on a module sees more than 60 N is the second or so when the lead wheels have entered the first module but the brush is still over the dock: about 73 N [C2]. That is within the 75 N that R10 allows for the row-entry transient (DRN-DDR-002, N2), and the steady brushing load of 59 N at worst tilt meets the 60 N steady limit. The wheel-load parts of R10 are met on paper, subject to the module maker's frame guidance; the 15 kg mass limit is not (section A).

*Table 4. Resistance and traction at 25° tilt, friction 0.4.*

| Case | Resistance | Traction available | Margin | Tag |
| --- | --- | --- | --- | --- |
| Still air (rolling 7.6 N, brush 30 N, 2° grade 5.5 N) | 43 N | 78 N | 1.79 | [C3] |
| 6 m/s wind along the row, start limit (16 N) | 60 N | 78 N | 1.30 | [C13] |
| 8 m/s wind along the row, abort limit (29 N on 0.50 m²) | 72 N | 78 N | 1.07 | [C4] |
| Friction 0.3 at 6 m/s | | | 0.98 | [C13] |
| Friction 0.3, still air and 8 m/s | | | 1.34 and 0.81 | [C5] |
| Friction 0.6, still air and 8 m/s | | | 2.69 and 1.61 | [C6] |
| 35° tilt, still air and 8 m/s | | | 1.66 and 1.00 | [C9] |

In still air the robot has a traction margin of 1.7 to 1.9 on all tilts from 10° to 35°. At the 8 m/s wind limit of R9 the margin falls to about 1.07 at 25° and 1.00 at 35°, and it drops below 1 if the friction is 0.3. A margin of 1.25 holds up to about 6.4 m/s at 25° and 5.6 m/s at 35° [C7]. DRN-DDR-002 therefore sets a start limit of 6 m/s at the dock anemometer, with 8 m/s kept as the abort limit at which the robot returns to the dock. At the start limit the margin is 1.30 at friction 0.4 but only 0.98 at friction 0.3 [C13], so R9 stays at risk until friction is measured.

**Frame steps and gaps (R4).** A 70 mm wheel meeting a 5 mm step touches its edge at 31°. With the lead wheel driven, the rest of the truck must add about 9 N at its axle, against about 12 N of spare traction on the other wheels [C10]. A 3 mm step needs about 2 N, and a 25 mm gap between modules lets the wheel dip only 2.3 mm [C11]. Steps of 5 mm are therefore marginal and R4 is at risk. The 18 mm tread sits 4 mm clear of the glass edge on a 25 mm frame flange; on modules whose visible flange is narrower than about 21 mm the tread would run on the glass [C12], so the flange width of target modules must be surveyed.

## D. Wind (R9)

*Table 5. Wind loads.*

| Case | Load | Held by | Tag |
| --- | --- | --- | --- |
| Parked, 35 m/s along the row | 555 N | 6 mm latch pin of the robot's solenoid in the dock latch tab, 2,827 N in shear (factor 5.1) | [D1, D2] |
| Parked, 35 m/s, lift on the robot | 260 N lift against 142 N weight; net 118 N up | Two hook rollers, about 119 N each with preload | [D1] |
| Parked, dock as a whole | 555 N from the robot plus 164 N on the panel | Two dock clamps, 3,000 N by friction (factor 4.2), plus the legs | [D2] |
| Running, 8 m/s | 14 N lift against 142 N weight | Weight alone | [D3] |
| End stop, IR sensing failed | 0.32 J impact, 127 N on a 5 mm buffer; then up to 78 N of drive stall | Stop clamp, 1,500 N by friction | [D4] |

The parked and end-stop cases meet R9 on paper with factors above 4. Running in wind is limited by traction (section C), not by lift.

## E. Chassis beam

The 40 x 80 x 2 mm beam spans 2.33 m between the truck plates. Carrying the brush, hood, pack, controller and wiring, plus a 250 N point load at mid-span (a person leaning on it), it is stressed to about 18 MPa, against a yield of about 160 MPa for 6063-T6, and deflects about 3.0 mm [E1]. The beam is not critical; a lighter section could be checked later.

## F. Power, cycle time and energy (R7, R8)

*Table 6. Power and energy per cycle.*

| Quantity | Value | Tag |
| --- | --- | --- |
| Electrical power while cleaning | 68 W (brush 48 W, drives 17 W, electronics 3 W) | [F1] |
| 40 m row (35 modules, 20.3 kWp) | 7.4 min; 7.7 Wh from the pack, 8.0 Wh from the dock | [F2] |
| 60 m row (52 modules, 30.2 kWp) | 10.6 min; 11.4 Wh from the pack | [F3] |
| 100 m row (87 modules, 50.5 kWp) | 17.4 min; 19.0 Wh from the pack, 19.8 Wh from the dock | [F4] |
| Three cycles on the 100 m row plus three days of standby | 68 Wh of 102 Wh usable (margin 1.51) | [F5] |
| Days with no sun on the 40 m row | 9 | [F5] |
| Dock harvest | 45 Wh/day at 3 sun hours; 82 Wh/day at 5.5 | [F6] |
| One 100 m day, from the dock | 23 Wh (margin 1.92 at 3 sun hours) | [F6] |

R7 is met (17.4 min against 20 min) and R8 is met. The cycle includes 30 s for the start warning, undocking and docking and 0.9 m of travel each way between the parked position and the row. The energy flow for one cycle on the 40 m row is 8.02 Wh from the dock, 7.70 Wh out of the pack, 0.37 Wh to the electronics, 7.33 Wh into the motors and 4.20 Wh at the brush and wheels [F7]; it is drawn in `media/flow.png`.

## G. Coverage (R5)

The brush covers 2,198 of the 2,228 mm of glass across the slope (98.7 %). At the far end the lead wheels stop against the end-stop buffers with the brush edge 85 mm short of the end of the glass. Over the 40 m row the brushed share of the glass is 98.4 % [G1]. R5 is met.

## H. Stopping (R12)

With power cut, the brush and the reflected inertia of its gearmotor coast to rest in about 0.13 s against the brush drag, and the robot stops in about 0.07 s on its own resistance [H1]. Adding a controller response of 0.1 s, both are well inside the 2 s of R12.

## I. Cost and payback (R13, R14)

The 16 BOM lines total $573.00 against the $500 value-engineering target, $73.00 over [I1], so R13 is over the target by USD 73. The $73 is the parts that make the design buildable (DRN-DDR-003): flange bearings, drive housings, couplings, roller clevises and sliders, dock brackets, clamps, ties and foot plates, the latch solenoid, beam cleats and other fittings. Every price is indicative. DRN-DDR-002 kept `budget_usd` at $500 as a hypothetical control target until quotes exist; the savings worth trying are in the value engineering section of DRN-DEC-001.

*Table 7. Recovered energy and simple payback on the $573 parts cost.*

| Case | Recovered energy | Value | Payback | Tag |
| --- | --- | --- | --- | --- |
| 40 m row, 0.3 %/day | 1,223 kWh/yr | $122/yr | 4.7 yr | [I2] |
| 40 m row, 0.49 %/day | 2,384 kWh/yr | $238/yr | 2.4 yr | [I3] |
| **60 m row, 0.3 %/day (R14 case)** | **1,816 kWh/yr** | **$181/yr** | **3.2 yr** | [I4] |
| 100 m row, 0.3 %/day | 3,039 kWh/yr | $304/yr | 1.9 yr | [I5] |

The robot shades each module for a few seconds in the evening, which costs 1 to 2 kWh a year [I2 to I5]. R14, as restated by DRN-DDR-001 (D8), is at risk at 3.2 years on the 60 m row (kept at 3 years and marked at risk by Amish on 2026-10-02; revisit when real quotes exist); the shortest row that pays back in 3 years at $573 has 55 modules, 63.5 m [I9]. Two cautions apply. If a $40 set of sleeves is needed every year, the 60 m payback becomes 4.0 years [I6]. And the result depends on R2: the 60 m row would meet 3 years only if daily dry cleaning held the residual loss below 1.3 % [I7], against the assumed 1.5 %. Each avoided monthly wash of the 40 m row saves about 122 to 350 L of water, 1.5 to 4.2 m³ a year [I8].

## J. Results against every requirement

*Table 8. Requirement status at TRL 3.*

| ID | Requirement | Target | Value (DRN-CAL-001) | Status |
| --- | --- | --- | --- | --- |
| R1 | Water-free cleaning | No water in normal operation | None by design | Met |
| R2 | Cleaning effectiveness | Residual loss 1.5 % or less at 0.3 to 0.5 %/day | Assumed; cannot be calculated | Not verifiable at TRL 3 |
| R3 | Glass and coating safety | Interference 3 to 5 mm; no hard parts within 10 mm | 3.5 to 4.4 mm [B5]; nothing but the brush within 10 mm [B6]; abrasion unknown | Not verifiable at TRL 3 (geometry met) |
| R4 | Fit the reference table | 25 mm gaps; 5 mm steps; tilt 10 to 35° | 5 mm step: 9 N needed, 12 N spare [C10]; flange width assumed [C12] | At risk |
| R5 | Coverage | 95 % or more | 98.4 % [G1] | Met |
| R6 | Rail-free installation | No rails, no drilling; 60 min for two people | Rail-free and clamp-on by design; time cannot be calculated | Not verifiable at TRL 3 |
| R7 | Cycle time | 100 m row in 20 min or less | 17.4 min [F4] | Met |
| R8 | Energy autonomy | Three 100 m cycles with no sun; recharge at 3 sun hours | 68 of 102 Wh [F5]; 45 Wh against 23 Wh a day [F6] | Met |
| R9 | Stay on the row | End stops; start below 6 m/s, abort at 8 m/s; survive 35 m/s parked | Parked and end stop hold with factors over 4 [D1 to D4]; traction margin 1.30 at 6 m/s [C13], 1.07 at 8 m/s [C4], friction 0.4; 0.98 at 6 m/s with friction 0.3 | At risk |
| R10 | Load on the modules | 16.5 kg or less (restated 2026-10-02); 60 N or less per wheel steady, 75 N at row entry | 15.9 kg [A3]; 59 N brushing at worst tilt [C8]; 73 N for about a second at row entry [C2] | Met on paper; weigh at TRL 4 |
| R11 | Environment | IP65; 0 to 50 °C ambient; glass to 75 °C | Pack in the sun may exceed its 45 °C charge limit; sunshade added | At risk |
| R12 | Safe to be near | Stop within 2 s; guards; stops on each truck | 0.13 s brush, 0.07 s robot [H1]; belt guards and a stop button in each truck plate | Met |
| R13 | Affordable | Parts at or below the $500 value-engineering target | $573.00 [I1] | Over the value-engineering target by USD 73 |
| R14 | Pays for itself | 3 years or less on rows of 60 m or more, mid case | 3.2 years [I4]; met from 63.5 m [I9]; 4.0 years with yearly sleeves [I6] | At risk (kept, not restated, 2026-10-02) |
| R15 | Serviceable | Sleeve change in 15 min on the row; catalog parts | Catalog parts; time cannot be calculated | Not verifiable at TRL 3 |

Counts: 6 met, 4 at risk, 1 short of target (R13 over the value-engineering target), 4 not verifiable at TRL 3, after Amish's decisions of 2026-10-02 on R10 and R14; `sizing.py` now prints the same counts [J0], having printed 5 met, 3 at risk, 3 not met and 4 not verifiable before them. Version 0.2 had 7 met, 4 at risk and none not met; R10, R13 and R14 changed with the constructable design (DRN-DDR-003), and R13 moved from at risk to over the value-engineering target.

## Checks against the TRL 2 figures (version 0.2 values)

| TRL 2 claim (DRN-PRC-001 v0.2) | TRL 3 value | Change |
| --- | --- | --- |
| Robot about 12 kg | 13.8 kg | Heavier: 50 mm core, plates and hood from the model |
| About 52 N per wheel with 50 N preload | 55 N brushing with 70 N preload; 72 N with the brush off the glass | The brush reaction was not in the TRL 2 figure |
| About 70 W while cleaning | 67 W | Brush 47 W, drives 17 W |
| About 7 min and 8 Wh on the 40 m row | 7.4 min and 7.6 Wh (7.9 Wh from the dock) | Docking time added |
| About 17 min and 20 Wh on a 100 m row | 17.4 min and 19.6 Wh from the dock | Row of 87 modules (100.4 m) |
| Traction about 83 N against 39 N (margin about 2) | 78 N against 43 N (margin 1.84) | Brush reaction lowers the wheel load |
| About 650 N along the row and 170 N net lift parked | 555 N along, 137 N net lift | Silhouette from the model |
| About 98 % coverage | 98.4 % | End-of-row strip included |
| About $485; payback about 4.0 years on the 40 m row | $500; 4.1 years on the 40 m row, 2.8 years on 60 m | Anemometer added; R14 restated |

## Checks against version 0.2 (design for construction)

| Version 0.2 value | Version 0.3 value | Why |
| --- | --- | --- |
| Robot 13.8 kg | 15.9 kg | Bearings, housings, brackets, cleats and fittings added by DRN-DDR-003 [A4] |
| Hook preload 70 N per truck | 60 N per truck | Same 60 N wheel-load rule with the heavier robot [C0] |
| 55 N per wheel brushing; 72 N at row entry | 56 N; 73 N | Heavier robot, lower preload |
| Traction margin 1.33 at 6 m/s (friction 0.4) | 1.30 | Heavier robot, lower preload |
| Beam span 2.32 m | 2.33 m | Truck plates 28 mm (was 22 mm) outboard of the frame, to fit the guide roller clevises |
| Parts $500.00 | $573.00 | Parts added for construction |
| Payback 2.8 years on 60 m | 3.2 years on 60 m; 3 years from 63.5 m | Higher parts cost |

