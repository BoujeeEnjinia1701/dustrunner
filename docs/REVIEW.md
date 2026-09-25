# Review note: DustRunner

## Session 2026-09-25: /populate to a strong TRL 2 (overnight batch run)

### What was done

- `docs/01-problem.md` (DRN-PRB-001 v0.2): problem with cited soiling and water figures, users and operating context, prior work (Ecoppia, NOMADD, SolarCleano, an academic prototype) with links, constraints including module warranty and live-array hazards, out of scope, open questions. There was no co-design checklist to keep.
- `docs/03-requirements.md` (DRN-REQ-001 v0.2): 15 measurable requirements (R1 to R15) against a defined 40 m, 20 kWp reference row, with a status column and assumptions.
- `docs/02-concept.md` (DRN-PRC-001 v0.2): how it works, numbered components, mass, power and energy per cycle, autonomy, traction, wind, recovered energy and payback, cost, design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model of a three-module section of the reference table (frames, glass, dust film, purlins, posts), the robot (beam, brush, hood, motors, end trucks, rollers, battery, controller, sensors), the clamp-on dock with its 20 W panel, and the end stops. Every robot and dock part carries a BOM number.
- `media/`: hero with a 1.75 m person, blueprint sheet (PNG, PDF, SVG), `model.glb` and `viewer.html`, exploded view with callouts 1 to 14, cutaway (section across the row at the lower module edge) and an energy flow diagram per cleaning cycle with estimated values. The exploded view and cutaway are rendered by the script with the kit's renderer so the robot is readable at a useful scale; temporary `_views` folders are removed.
- `bom/bom.csv`: 15 lines with indicative prices, numbered to match the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image, links line, concept paragraph and key components updated.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Robot mass | about 12 kg; about 52 N per wheel on the frames with hook preload | R10 met on paper |
| Power while cleaning | about 70 W (brush 50 W, drives 16 W, electronics 3 W) | |
| 40 m row, out and back | about 7 min, about 8 Wh from the dock | |
| 100 m row, out and back | about 17 min, about 20 Wh | R7 met |
| Autonomy | about 102 Wh usable; about 5 days on a 100 m row with no sun | R8 met |
| Dock panel harvest | about 82 Wh/day at 5.5 sun hours, 45 Wh/day at 3 | R8 met |
| Coverage | about 98 % of the glass across the slope | R5 met |
| Traction | about 83 N available against about 39 N needed (both wheels driven, 50 N hook preload per truck, friction 0.4 assumed) | Margin about 2, unverified |
| Wind while cleaning | stop above 8 m/s; parked at 35 m/s about 650 N along the row and 170 N net lift | R9 unverified |
| Recovered energy, mid case | about 1,220 kWh a year, about $120 a year | |
| Payback | about 4.0 years mid case; about 2.0 years at 0.49 %/day; about 1.6 years on a 100 m row | **R14 not met** in the mid case |
| Parts cost | about $485 for robot and dock | R13 met, about 3 % margin |

Requirements not met or not shown:

- **R14 (payback within 3 years) not met** in the mid case on the 40 m reference row: about 4 years.
- **R2 (cleaning effectiveness) not shown:** the 1.5 % residual loss with daily dry cleaning is an assumption; dew-cemented dust may not come off dry.
- **R3 (glass and coating safety) not shown:** long-term abrasion from daily microfiber contact is unknown, and some module makers require approval of motorized cleaning tools.
- **R9 (wind) unverified:** the operating wind limit needs a wind input that is not in the BOM.
- **R13 margin is thin:** an anemometer would bring the cost to about $500.

### Proposed, awaiting Amish

1. **Scope: one full-width robot per row, riding on the frames of 1P portrait tables.** Options: (a) as proposed; (b) a smaller robot that moves on the glass; (c) add a transfer cart between rows. Recommendation: (a). This limits fit to tables whose short module edges are free of clamps.
2. **Cleaning time.** Options: night (as Ecoppia does), evening before dew forms, or dawn. Recommendation: evening, gated by the humidity sensor.
3. **Wind input.** Options: (a) anemometer at the dock (about $15, cost about $500); (b) a weather feed over the network; (c) a fixed wind rule from motor current. Recommendation: (a).
4. **Charging at the dock rather than a panel on the robot.** Recommendation: dock panel, 20 W.
5. **Traction: both wheels driven on each truck and spring-preloaded hook rollers.** Recommendation: yes, pending friction measurement.
6. **12.8 V LiFePO4, 10 Ah.** A SwapCell pack is not proposed because DustRunner needs about a quarter of its energy at a quarter of its voltage. Recommendation: LiFePO4.
7. **Reference row for requirements and payback.** 40 m and 20 kWp is proposed. A 100 m reference would meet R14; that choice changes how the pitch is judged, so it is Amish's.
8. **R14 target.** Options: keep 3 years and accept that the reference row does not meet it; relax it to 5 years; or restate it per row length. Recommendation: restate it as "3 years or less on rows of 60 m or more".
9. **Pilot site and partner** (solar pumping farm, mini-grid operator or university test array).
10. **Budget.** Parts cost is within `budget_usd` ($500); no change proposed. `project.yaml` is unchanged, including `pitch` and `problem`: the "15 to 25 %" figure matches arrays left a month or more in the dusty season (QEERI about 13 % a month, Arar 11 to 18 % a month in summer), and DRN-PRB-001 now states that context. A more precise wording ("up to 15 to 25 % a month in the dusty season") is suggested for Amish to consider.

### Safety concerns

- Rotating brush, belts and wheels on an unattended machine that starts on a timer: guards, emergency stops on both trucks, an audible start warning and a lockout at the dock.
- A 12 kg robot falling from up to 1.6 m if it leaves the row end or is lifted by wind: two independent end stops and hook rollers; wind loads unverified.
- Live PV strings at several hundred volts DC that cannot be switched off in daylight: the robot must never touch cables, connectors or junction boxes; damaged glass exposes live parts.
- LiFePO4 pack: BMS, fused output, no charging below 0 °C, shaded and ventilated.
- Hot glass and frames up to about 75 °C during installation and service.
- Module warranty risk from abrasive cleaning or cleaning tools the maker has not cleared.

### Problems and notes

- The kit's default scale figure stands in front of the table's lower edge, where it hid the robot's lower end and the dock, so the script places the 1.75 m person itself as a context part standing on the ground beyond the far end of the row.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).
- Suggestion, not done: a soiling-station measurement at the pilot site before any build would answer R2 and R14 at low cost.

### Recommended next step

Review this note and the media, then decide items 1, 3, 7 and 8. If approved, run `/advance-trl3` to check the brush power, traction, wind and frame-load estimates by calculation and produce the parametric model and drawing sheet.
