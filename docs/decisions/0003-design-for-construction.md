---
doc_id: DRN-DDR-003
title: DustRunner design for construction
project: DustRunner
doc_type: Design decision record
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: Accepted by Amish on 2026-10-02, including the recommendations for A2 to A4
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Consequences updated: appearance model brought into line with the constructable design'
---

# 0003: Design for construction

- **Date:** 2026-09-30
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations in Table 3 (A2 to A4), which are now decided as recommended and recorded in the design decisions register (DRN-DEC-001).

## Context

On 2026-09-30 Amish asked for the build plan to show how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of DRN-CAL-001 v0.2 showed what DustRunner does but was a massing model: checking it with build123d (overlap volumes and gaps between solids) found parts that floated, rubbed, blocked each other or had no fixing. Problems P1 to P16 below are the ones found.

The changes keep what DustRunner does: the same full-width brush and its interference, the same wheels on the frame top flange, guide rollers on the frame face and sprung hook rollers under the bottom flange, the same pack, controller, sensors, dock with panel, contacts, latch and anemometer, and the same clamp-on end stops. The pitch and the safety case are unchanged; every guard and stop of the concept is still there, and the belts are now fully enclosed. Every change is in `cad/src/model.py`, which now runs 123 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must stay apart are apart by at least the stated clearance, including the robot parked in the dock, at the end stop and on the module. All 123 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The 22 mm guide rollers filled the 22 mm gap between the truck plate and the frame face: each roller rubbed the plate, and nothing held its axle. | Plate gap 28 mm (was 22). Each roller turns on an M8 bolt in a folded 3 mm aluminium clevis screwed to the plate's inner face; it bears on the frame and stands 6 mm off the plate. | A clevis is the simplest bracket that carries a roller on both sides of its axle. 6 mm more gap is the least that fits the clevis back and a clearance. |
| P2 | The hook roller floated 2 mm above a rigid hook arm that was part of the plate; it had no axle and no spring, so the 70 N preload had no mechanism. | A 10 mm aluminium slider runs up and down the plate's inner face on two M6 shoulder bolts; the roller turns on an 8 mm axle cantilevered from it under the frame; a compression spring on a seat bracket pushes the slider up. The plate is 24 mm taller (296 mm) to carry the seat. | A slider and spring give a set preload that follows small frame height changes and can be backed off to fit the robot. Cantilevering the axle keeps everything under the flange inside the frame's 3 to 21 mm band and clear of the dock. |
| P3 | The wheel axles were stubs on the plate's inner face, yet a belt on the outer face linked them; a driven axle cannot be carried by a 5 mm plate alone. | Each 10 mm axle turns in two 2-bolt flange bearings, one each side of the plate; the pulley sits outboard. | Two bearings a plate's width apart carry the overhung wheel and the belt pull. |
| P4 | Both gearmotors and the brush motor floated outboard of the trucks with no fixing; the wheel belt passed through the brush shaft. | A folded aluminium drive housing on each truck (2 mm at the lower truck, 1.5 mm at the upper) covers the belts and carries the motors, face-mounted on its outer wall. The drive motor joins its axle through a shaft coupling. The wheel and brush belts run in separate layers; the brush stub shaft steps from 20 to 15 mm outboard of the plate to clear the wheel belt by 2.5 mm. | One part guards the belts (pinch points, R12) and mounts the motors. |
| P5 | The brush shafts butted against the core ends and passed through the plates with no bearing. | Turned aluminium end plugs pressed into the core; stub shafts pressed into the plugs; one 20 mm bore 2-bolt flange bearing on each plate's inner face. | The two "sealed bearings" of BOM line 2, made into parts that can be bolted on. |
| P6 | The beam butted against both plates with no fixing. | Two 30 x 30 x 3 mm angle cleats at each beam end, through-bolted across the beam and bolted to the plate. | Bolted cleats can be undone to change the module length (cut a new beam). |
| P7 | The hood floated 3 mm below the beam; the sunshade floated 6 mm above the pack. | Five 3 mm nylon spacers and M5 screws into rivet nuts in the beam's bottom wall hang the hood; four 12 mm tube posts on M5 screws carry the sunshade 6 mm above the pack. Two straps hold the pack to the beam. | Keeps the gaps the concept intended (hood clearance, air under the shade) with plain fixings. |
| P8 | The IR sensors and the robot's contact pad were butted against the plate's end edge. | Folded 3 mm brackets screwed to the plate's inner face carry the sensors 44 mm above the frame, and a folded bracket carries the robot contact block. | Brackets on the face, not the edge. |
| P9 | The dock latch had no parts: the dock's "latch with a 6 mm pin" had nothing to engage on the robot, and no way to release. | A 12 V spring-return pull solenoid on the robot's contact bracket: its 6 mm pin drops through a hole in a 6 mm latch tab on the dock contact block when the robot parks, and the robot lifts it for about a second to leave. The tab's free end is chamfered so the pin rides up onto it. | Keeps the 6 mm pin in shear that DRN-CAL-001 [D2] checks. A sprung pin that drops in by itself fails safe (latched); the robot already has power and a controller to lift it, so the dock needs no new electronics. |
| P10 | The dock contact block floated 89 mm above the dock frame. | A 40 x 20 mm tube contact post bolted to the rail-start cross member carries the dock contact block, with the latch tab on top. | Places the contacts where the robot's block arrives, 2 mm apart when parked. |
| P11 | Two dock posts sat under the rails in the hook roller's path, so the robot could not leave the dock; the cross members did not reach the rails; the clamps were connected to nothing. | Cross members are 40 x 40 x 2 mm tube, 6 mm below the rail bottom and starting 30 mm inside the rail, clear of the hook roller path. Each rail is held by folded 4 mm L brackets inside the channel (screwed through the web with flush countersunk screws) and bolted down through a spacer (rail-start member) or a shim on a clamp bar (near member). | The robot's wheels, guide rollers and hook rollers wrap all three outside faces of the rail, so a rail can only be held from inside its channel. |
| P12 | The dock clamps did not grip the module frame. | Each frame clamp is a 40 x 6 mm bar under the first module's long-side bottom flange and a 6 mm jaw on top of the flange inside the frame, with a 2.5 mm spacer beside the flange edge and one M8 bolt. The bar's other end bolts to the near cross member. | Grips the frame's return flange without drilling (R6). |
| P13 | The dock legs met the tilted cross members at an angle with no fixing, and stood on nothing. | 40 x 40 x 2 mm square-tube legs stand vertical beside the far and rail-start cross members, bolted through both with two M8 bolts, on 100 x 100 x 6 mm foot plates. Three 40 x 20 mm ties on top join the far and rail-start members and carry the panel. | Side-by-side bolting works at any tilt; the ties make the dock one frame and give the panel its mounting. |
| P14 | The anemometer mast stood normal to the tilted table, 25° off vertical. | The mast is vertical, held by two U-bolt clamps on the far cross member. | Cup anemometers are made to read with a vertical axis. |
| P15 | The end stop was taller than the IR sensors' height, so a sensor housing hit it before anything else; it had no clamp screw. | End stop made of three screwed pieces (top block, outer plate, bottom jaw) with an M8 clamp screw up against the frame's bottom flange; its top is 40 mm above the glass, so the sensors pass 5 mm over it and the wheels meet the rubber buffer. | The wheel tyre and buffer take the impact [D4]; the sensors are not a structural stop. |
| P16 | The module's long-side frames were modelled solid, so the clamp had nothing to grip. | Reference module ends modelled as C sections like the edges (context only, not in the BOM). | Makes the frame clamp's fit checkable. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | 15.9 kg (was 13.8 kg): parts added for construction about 2.1 kg [A4]. | Bearings, housings, brackets, clamps and fittings that the massing model left out. |
| Hook preload | 60 N per truck (was 70 N), set by the same rule as before: the highest preload that keeps the steady brushing wheel load at 60 N or less at every tilt [C0]. Wheel loads 56 N brushing at 25°, 59 N worst tilt, 73 N at row entry; traction margin 1.30 at the 6 m/s start limit (was 1.33). | The heavier robot presses harder on the frames, so less spring is needed for the same wheel load. |
| Beam and span | Beam 2,334 mm (was 2,322); plates 28 mm outboard of the frame. Robot 2,556 mm across the slope with the motors (was 2,488). | Plate gap and drive housings. |
| Cost | BOM lines 2, 5, 7, 11, 13, 14, 15 and 16 repriced: $573.00 (was $500.00) [I1]. Payback on a 60 m row 3.2 years (was 2.8); 3 years from 63.5 m [I9]. | Parts added for construction. |
| Drawing | DRN-DWG-001 Rev P3; making sketches DRN-DWG-101 to 119 added. | Follows the model. |
| Documents | DRN-CAL-001 v0.3, DRN-REQ-001 v0.5, DRN-PRC-001 v0.5 updated. R10 (mass), R13 and R14 now not met; no target changed. | Follows the model. |
| Wind, stopping, energy | Parked and running wind checks still hold with factors over 4; brush and robot stop in 0.13 and 0.07 s; 68 W cleaning, 7.7 Wh per 40 m cycle. | Recalculated in DRN-CAL-001 v0.3. |

*Table 3. Items that change a requirement: proposed, then accepted by Amish as recommended on 2026-10-02 (A1 is a value-engineering note, not a decision).*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Parts now cost $573 against the value-engineering target of $500 (`budget_usd`, a hypothetical control target), USD 73 over. | No decision needed. The target stays $500; savings worth trying at quotes are cheaper bearings and a lighter dock. | Carry in the value engineering section of DRN-DEC-001. |
| A2 | The robot weighs 15.9 kg against R10's 15 kg, though every wheel load meets R10. | (a) restate R10's mass limit as 16.5 kg, keeping the 60 N and 75 N wheel-load limits that protect the modules; (b) find about 1 kg (4 mm truck plates, pocketed plates, 1.5 mm lower housing); (c) both: restate now, weigh at TRL 4. | (c). Accepted 2026-10-02: R10's mass limit is 16.5 kg, wheel-load limits unchanged. |
| A3 | At $573 the payback on a 60 m row is 3.2 years (R14 not met); 3 years needs a row of about 64 m. | (a) restate R14 as "3 years or less on rows of 65 m or more"; (b) keep R14 and treat it as at risk until quotes; (c) relax it to 3.5 years on 60 m. | (b), revisited once quotes exist. Accepted 2026-10-02: R14 is kept and marked at risk. |
| A4 | Latch release: the robot lifts its own latch pin with a solenoid (P9). | (a) robot-side solenoid as modelled; (b) solenoid on the dock, switched through a fourth contact; (c) a passive latch the robot pulls out of with its drives (no pin in shear, so the parked wind case must be rechecked). | (a). Accepted 2026-10-02. |

## Consequences

- With A2 to A4 accepted (2026-10-02): R10's mass limit is restated as 16.5 kg (DRN-REQ-001), so the 15.9 kg robot meets it on paper and is weighed at TRL 4; R14 stays at 3 years on rows of 60 m or more and is at risk until quotes; the robot-side solenoid stays as drawn.

- `design_state: constructable` in `project.yaml`. The build plan DRN-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`). Open decisions are in the design decisions register DRN-DEC-001.
- Requirement status (DRN-CAL-001 v0.3): 5 met, 3 at risk (R4, R9, R11), 3 not met (R10 on mass, R13, R14), 4 not verifiable at TRL 3. Before: 7 met, 4 at risk, none not met.
- The appearance model `cad/src/product_model.py` now takes the trucks, hook arms, dock, legs and mast from the constructable design in `cad/src/model.py`. The photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` are made from it on Amish's Mac, where Blender is.
- The module frame's bottom flange width and the room above it for the clamp jaw, and the parts' real masses, are checked when parts are bought (TRL 4).
