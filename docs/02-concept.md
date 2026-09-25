---
doc_id: DRN-PRC-001
title: DustRunner design precis
project: DustRunner
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, traction, wind, economics, safety, media)
---

# DustRunner design precis

## Summary

DustRunner is a rail-free crawler robot that spans one PV table from its lower to its upper module edge, rides along the module frames on two end trucks that hook under the frame lips, and sweeps the glass dry with a 2.2 m rotating microfiber brush. It parks off the glass in a clamp-on dock at the start of the row, where a 20 W panel recharges its 12.8 V LiFePO4 pack. First-order estimates for a 40 m, 20 kWp reference row: about 7 minutes and 8 Wh per out-and-back cycle, a robot of about 12 kg, and about $485 in parts for robot and dock. The weak points are traction on dusty frames, wind, unproven cleaning effectiveness and glass abrasion, and a payback of about 4 years in the mid case (R14 not met).

![Hero render](../media/hero.png)

*Figure 1. DustRunner partway along a three-module section of the reference table, moving away from its dock (brown, left) toward the end stops (red). Glass behind the robot is clean; tan shows dust still to be removed. Grey figure: 1.75 m person for scale.*

## How it works

1. **Park and charge.** Between cycles the robot sits in the dock, a short pair of rails that continue the module edges past the end of the row. Parking off the glass means the robot never shades the array. A 20 W panel in the dock charges the pack through spring contacts.
2. **Start.** Once a day, after the array's output has dropped in the evening and before dew forms (proposed, awaiting Amish), the controller checks pack charge, air humidity and a wind limit, then drives out of the dock.
3. **Travel.** Two end trucks carry the robot along the row. Each truck has two polyurethane wheels on the top of the module frame, two guide rollers against the outer face of the frame and a spring-loaded hook roller under the frame lip. The trucks are the "clamp": they cannot lift off or slide down the slope, yet need no rail. A drive gearmotor with an encoder on each truck drives both of that truck's wheels through a toothed belt, and the controller keeps the two ends in step.
4. **Clean.** A 120 mm microfiber brush on a 2.2 m aluminum tube spans the slope and turns at about 150 rpm, lifting dust ahead of the robot. A helical pattern on the brush conveys the loosened dust down the slope and off the lower edge. A hood over the brush limits dust thrown back onto clean glass.
5. **Stop and return.** IR sensors on each truck see the frame end; a clamp-on end stop at the far end is the mechanical backstop. The robot reverses the brush and cleans on the way back, then docks.

![Energy flow](../media/flow.png)

*Figure 2. Energy for one out-and-back cycle on the 40 m reference row, in Wh. All values are estimates.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Chassis beam | 40 x 80 mm aluminum rectangular tube, about 2.3 m | Cut to the module length for other tables |
| 2 | Microfiber brush | 120 mm diameter, 2.2 m, on a 40 mm aluminum tube | Replaceable microfiber sleeves with a helical pattern |
| 3 | Brush hood | Bent 1 mm aluminum or polycarbonate half-shell | Also the finger guard at the brush ends |
| 4 | Brush motor and belt drive | 12 V DC gearmotor, about 60 W, toothed belt | Reversible; about 150 rpm at the brush |
| 5 | End trucks and wheels | 6 mm aluminum plates, two 70 mm polyurethane wheels each, belt-linked | Wheels run on the frame top only |
| 6 | Drive gearmotors | Two 12 V gearmotors with encoders, one per truck | Synchronized in firmware |
| 7 | Guide and hook rollers | Sealed-bearing rollers: guide rollers on the frame face, spring-loaded hook rollers under the lip | Keep the robot on the table in wind |
| 8 | Battery | LiFePO4, 12.8 V, 10 Ah (128 Wh) with BMS | Chemistry chosen for heat tolerance and safety |
| 9 | Controller | ESP32-class board, two drive channels, brush driver, current sensing, humidity and temperature sensor, IP65 box | Firmware is a sketch until TRL 4 |
| 10 | IR edge sensors | Four downward-looking reflective sensors, two per truck | Row-end and gap detection |
| 11 | Dock frame | Aluminum angle rails continuing the module edges, cross members, two clamps to the first module frame and four legs | Clamp-on; no drilling |
| 12 | Dock PV panel | 20 W, about 530 x 350 mm, in the table plane | Charges the parked robot |
| 13 | Dock charger and contacts | LiFePO4 charge controller and spring contacts | |
| 14 | End stops | Pair of clamp-on blocks on the last module's frame | Mechanical backstop |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM. The robot is laid flat in the table plane; the dock and end stops are drawn beside it. Upper-end twins of paired parts are shown without numbers.*

![Cutaway](../media/cutaway.png)

*Figure 4. Section across the row through the robot at the lower module edge, showing how the end truck wraps the frame.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

### Reference row and robot mass

| Quantity | Estimate | Basis |
| --- | --- | --- |
| Reference row | About 40 m, 35 modules, about 90 m² of glass, about 20 kWp | 35 x 1,154 mm pitch; 2,278 x 1,134 mm modules at about 580 W |
| Robot mass | About 12 kg | Beam 3.1 kg, brush 2.3, trucks and wheels 2.0, motors 1.2, battery 1.3, hood 0.7, rollers 0.4, controller 0.4, sensors and wiring 0.5 |
| Load normal to the glass | About 107 N | 12 kg x 9.81 m/s² x cos 25° |
| Load down the slope | About 50 N | 12 kg x 9.81 x sin 25°, carried by the upper truck's guide rollers |
| Wheel load | About 27 N, or about 52 N with 50 N of hook preload per truck | (107 N + 100 N) / 4 wheels |

The wheel loads are small next to the loads modules are rated for (for example the 2,400 Pa test load on about 2.6 m² is about 6 kN), but they act on the frame edge, so the module maker's guidance on frame loading must be checked (R10).

### Power and energy per cycle

Assumptions: travel 0.2 m/s; brush surface speed about 0.94 m/s (120 mm at 150 rpm); brush drag about 30 W of mechanical power (the largest uncertainty, to be measured); gearmotor and belt efficiency 60 % for the brush and 50 % for the drives; controller and sensors 3 W.

| Quantity | Estimate | Basis |
| --- | --- | --- |
| Brush tangential force | About 32 N | 30 W / 0.94 m/s |
| Drive force, worst case | About 39 N | Rolling 2 N (0.02 x 107 N), brush reaction 32 N, 2° row grade 4 N, roller drag 1 N |
| Power at the wheels | About 8 W | 39 N x 0.2 m/s |
| Electrical power while cleaning | About 70 W | Brush 50 W, drives 16 W, electronics 3 W |
| Cycle time, 40 m row out and back | About 7 min | 80 m / 0.2 m/s = 400 s |
| Pack energy per cycle, 40 m row | About 7.7 Wh (8.2 Wh from the dock) | 69 W x 400 s |
| Cycle time and energy, 100 m row | About 17 min, about 20 Wh from the dock | R7 met |
| Cleaning rate | About 1,600 m² per hour of travel | 2.2 m x 0.2 m/s |

### Charging and autonomy

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Usable pack energy | About 102 Wh | 128 Wh x 80 % | |
| Days of cleaning with no sun, 40 m row | About 13 | 102 / 7.7 Wh | |
| Days of cleaning with no sun, 100 m row | About 5 | 102 / 19.2 Wh | R8 met |
| Dock panel harvest | About 82 Wh/day at 5.5 sun hours; about 45 Wh/day at 3 | 20 W x hours x 0.75 | R8 met |

The pack is cycled lightly (under 10 % of capacity a day on the reference row), which is kind to LiFePO4 cells in heat. A smaller 6 Ah pack would work on rows under about 60 m; the 10 Ah pack is kept for longer rows and cloudy spells.

### Traction

Traction is the tightest mechanical margin. If only one wheel per truck were driven, the driven wheels would carry about 54 N, and at an assumed friction coefficient of 0.4 for polyurethane on a dusty anodized frame they could push only about 21 N against the 39 N needed. Driving both wheels on each truck and preloading the hook rollers against the frame lip with springs raises the normal force to about 207 N and the available traction to about 83 N, a margin of about 2. The friction coefficient on dusty frames is an assumption and must be measured.

### Wind

| Case | Estimate | Consequence |
| --- | --- | --- |
| Along-row wind at 8 m/s while cleaning | About 34 N on about 0.58 m² of robot side area (drag coefficient 1.5) | Total drive force about 73 N, within the 83 N available; stop cleaning above 8 m/s |
| Parked in the dock at 35 m/s | About 650 N along the row; about 280 N of lift against about 107 N of weight | Dock latch and hook rollers must hold about 650 N along and about 170 N up |

A wind limit therefore needs a wind input: an anemometer at the dock (about $15 more), or a weather feed. This is an open question.

### Energy recovered, water saved and payback

Assumptions are listed in DRN-REQ-001: 5.5 kWh per kWp per day, a manual wash every 30 days as the baseline, $0.10/kWh, and an average residual loss of about 1.5 % with daily dry cleaning (unverified, R2).

| Case | Average loss, monthly wash | Average loss, daily DustRunner | Recovered energy | Value | Simple payback on $485 |
| --- | --- | --- | --- | --- | --- |
| Mid, 0.3 % per day, 40 m row | About 4.5 % | About 1.5 % | About 1,220 kWh a year | About $120 a year | **About 4.0 years (R14 not met)** |
| High, 0.49 % per day, 40 m row | About 7.4 % | About 1.5 % | About 2,390 kWh a year | About $240 a year | About 2.0 years |
| Mid, 100 m row | About 4.5 % | About 1.5 % | About 3,030 kWh a year | About $300 a year | About 1.6 years |

Water saved is about 120 to 350 L per avoided wash of the reference row (3.5 to 10 L per module), about 1.5 to 4 m³ a year for monthly washing. The case is strongest for long rows, for sites that currently do not clean at all, and for mini-grids where each kilowatt-hour displaces diesel.

### Cost

| Group | Indicative cost |
| --- | --- |
| Robot (items 1 to 10) | About $353 |
| Dock and end stops (items 11 to 14) | About $102 |
| Wiring, fuse, stop buttons and hardware (item 15) | About $30 |
| **Total** | **About $485 (R13 met, about 3 % margin)** |

## Key design choices

Every choice below is **Proposed, awaiting Amish**.

- **One robot per row, spanning the full slope.** A full-width robot needs no steering on the glass and cannot fall between modules. The alternatives are a smaller robot that zigzags on the glass (needs edge sensing on all sides and loads the glass) or a transfer cart that carries one robot between rows (more cost and complexity). Recommendation: one full-width robot per row.
- **Ride on the frame edges, not on the glass.** Wheels on the frame keep weight off the glass and coating. This limits the concept to tables whose short edges are free of clamps (1P portrait with clamps on the long sides, as on the reference table). Recommendation: frame riding, with the fit limit stated in R4.
- **Rail-free, with a short dock and clamp-on end stops.** The dock and stops are the only added hardware and clamp on without drilling. Fully rail-free operation with no end stop would rely on the IR sensors alone. Recommendation: keep the mechanical end stops as the independent backstop (R9).
- **Dry microfiber brush, no water and no airflow.** Microfiber is the gentlest common dry medium; an airflow stage (as Ecoppia uses) would add a fan and power. Recommendation: microfiber brush first; airflow only if tests show dust is re-deposited.
- **Charging at the dock, not from a panel on the robot.** A panel on the robot (as Ecoppia uses) needs no contacts but adds mass and wind area. Recommendation: 20 W dock panel.
- **Both wheels driven on each truck, with preloaded hook rollers.** See Traction. Recommendation: belt-linked wheels and spring preload.
- **Cleaning time.** Options: at night (no shading, cool glass, but dew can turn dust to mud), in the evening before dew forms (low shading loss), or at dawn (worst dew). While on the glass the robot shades a strip along one module, which can bypass a cell substring for a minute or two. Recommendation: evening, gated by the humidity sensor.
- **LiFePO4 at 12.8 V.** Safer and more heat-tolerant than lithium-ion NMC, and 12 V motors and chargers are common. Recommendation: 12.8 V LiFePO4. A SwapCell pack is not proposed: at about 468 Wh and 48 V it is far larger than DustRunner needs.
- **Budget.** Indicative parts cost is about $485 against the $500 budget; an anemometer would bring it to about $500. `project.yaml` is unchanged.

## Safety

> **Safety:** DustRunner is moving machinery with a rotating brush, a lithium iron phosphate battery, and it works on an energized PV array that can carry several hundred volts DC, on hot glass, up to about 1.6 m above the ground.

- **Rotating brush and pinch points.** The brush, belts and wheels can catch fingers, hair and clothing. The hood covers the brush ends; each truck has an emergency stop button; the brush stops when a truck lifts off the frame. Nobody should reach under the hood while the robot is powered.
- **Unexpected start.** The robot runs on a timer with nobody present. It must carry a clear warning label, start only after a short audible warning, and have a lockout switch at the dock.
- **Falling robot.** A 12 kg robot leaving the row end could injure someone below. Two independent stops (IR sensing and the mechanical end stop) and the hook rollers address this (R9); the design must be checked for wind at TRL 3.
- **PV array electrical hazard.** Strings carry DC voltages that can be lethal and cannot be switched off in daylight. Nothing on the robot may touch cables, connectors or junction boxes; installation and maintenance follow the array owner's electrical safety rules. Damaged module glass exposes live parts.
- **Battery.** LiFePO4 is less prone to thermal runaway than other lithium-ion chemistries but can still vent and burn if crushed, shorted or overcharged. Use a pack with a BMS, fuse the pack output, block charging below 0 °C, and keep the pack shaded and ventilated.
- **Hot surfaces.** Module glass and frames can reach about 75 °C. Wear gloves when installing or servicing in daylight.
- **Module warranty.** Abrasive cleaning, or a cleaning tool the maker has not cleared, can void the module warranty. Check the maker's cleaning guidance and ask the maker to clear the robot before use (see DRN-PRB-001).

## Open questions

- [ ] Brush drag power and cleaning effectiveness on real dust, dry and after dew (R2).
- [ ] Long-term abrasion of anti-reflective coatings by daily microfiber contact (R3).
- [ ] Friction coefficient of polyurethane on dusty frames; spring preload value (Traction).
- [ ] Wind input for the operating limit: anemometer at the dock or weather feed?
- [ ] Module makers' positions on frame loading and robotic dry cleaning.
- [ ] How dust conveyed off the lower edge builds up at the lower frame lip over time.
- [ ] Pilot site, partner and first table format (see DRN-PRB-001).
