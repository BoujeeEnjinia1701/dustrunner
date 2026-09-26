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

Status update: items 1 to 8 and 10 were decided by Amish, 2026-09-25: go with recommendation (DRN-DDR-001, D1 to D12). Item 9 has no recommendation and stays proposed, awaiting Amish.

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

## Session 2026-09-25: TRL 3

Amish approved all TRL 2 recommendations on 2026-09-25 ("proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them."). This session advanced DustRunner to TRL 3 and stopped there.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (DRN-DDR-001 v0.1): decisions D1 to D12 recorded as "Decided by Amish, 2026-09-25: go with recommendation"; O1 (pilot partner) left open.
- `docs/01-problem.md`, `docs/02-concept.md`, `docs/03-requirements.md` revised to v0.3: problem line reworded, design choices no longer "proposed", R14 restated for rows of 60 m or more, R13 now covers the anemometer, every number replaced by DRN-CAL-001 values.
- `docs/04-calcs/01-sizing.md` (DRN-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: mass, brush contact and core deflection, wheel loads, traction, frame steps, wind, beam, energy, coverage, stopping, cost and payback, with a status for every requirement. The script imports the model and reads the BOM and budget.
- `cad/src/model.py`: parametric build123d model (robot, dock, end stops, reference module) exporting `cad/step/dustrunner-{robot,dock,end-stop,assembly}.step` and `cad/stl/dustrunner-{robot,dock,end-stop}.stl`.
- `cad/src/sheets.py` and `cad/drawings/DRN-DWG-001.{svg,pdf,png}`: general arrangement at Rev P1 (top and front views at 1:20, section A-A at 1:5, isometric, interface notes), marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet stays DRN-DWG-010, so DWG-001 was free.
- `bom/bom.csv`: 16 lines, all priced with a supplier type; item 16 (dock anemometer) added. `bom/bom-notes.md` updated.
- `cad/src/concept_media.py` now builds the robot, dock and end stops from `model.py`; all media re-rendered and checked (hero, blueprint, exploded with callout 16, cutaway, flow, GLB and viewer). No `_views` folders remain.
- `project.yaml`: `trl: 3`, `trl_target: 3`, `trl_evidence` lists the docs, DDR, CAL note and script, model, STEP files, drawing and BOM; problem line reworded. `README.md` matches.

### Requirements at TRL 3 (DRN-CAL-001, Table 8)

Six met, five at risk, none not met, four not verifiable at TRL 3.

| Status | Requirements |
| --- | --- |
| Not met | None |
| At risk | R4 (5 mm frame step: 9 N needed, 14 N spare; tread needs a frame flange of about 21 mm or more); R9 (traction margin 1.10 in an 8 m/s wind along the row at friction 0.4, 0.82 at friction 0.3); R10 (13.8 kg and 58 N per wheel brushing, but about 72 N for about a second at row entry); R11 (pack may exceed its 45 °C charge limit in the sun); R13 ($500.00 against $500, no margin) |
| Not verifiable at TRL 3 | R2 (cleaning effectiveness), R3 (abrasion; the geometry is met), R6 (installation time), R15 (sleeve change time) |
| Met | R1, R5 (98.4 %), R7 (17.4 min), R8 (67 of 102 Wh), R12 (0.13 s), R14 (2.8 years on a 60 m row) |

Key numbers: robot 13.8 kg; 67 W while cleaning; 7.4 min and 7.6 Wh per cycle on the 40 m row; 17.4 min on a 100 m row; parked at 35 m/s, 555 N along the row and 137 N net lift, held with factors over 4; payback 4.1 years on the 40 m row, 2.8 years on 60 m, 3.5 years on 60 m if sleeves are replaced every year.

Changes forced by the calculations: the brush core grows from 40 to 50 mm (a 40 mm core lets the interference fall to 2.8 mm mid-span, outside R3); hook preload set at 70 N per truck (highest value keeping brushing wheel loads at 60 N or less); hood thinned to 0.8 mm; a sunshade added over the pack. Mass rose from about 12 kg to 13.8 kg.

### Decisions recorded

D1 to D12 in DRN-DDR-001: full-width robot on 1P frames; evening cleaning gated by humidity; anemometer at the dock; 20 W dock charging; both wheels driven with preloaded hook rollers; 12.8 V LiFePO4, no SwapCell; 40 m reference row kept; R14 restated for rows of 60 m or more; budget kept at $500 with the problem line reworded; 1P portrait 2,278 mm modules first; mechanical end stops kept; dry microfiber without airflow. The SwapCell interface v0.3 items do not apply because DustRunner uses its own pack.

### Proposed, awaiting Amish

1. **Pilot site and co-design partner (O1).** No recommendation; to be picked per area later. Still proposed, awaiting Amish.
2. **Start wind limit (new, from C4 and C7).** Options: (a) keep 8 m/s and accept a traction margin of about 1.1; (b) start a run only below 6 m/s at the dock anemometer and keep 8 m/s as the abort limit; (c) raise the hook preload, which breaks the 60 N wheel-load target. Recommendation: (b), revisited once friction is measured. This changes the R9 target, so it is Amish's. **Decided by Amish, 2026-09-25: go with recommendation** (DRN-DDR-002, N1).
3. **Row-entry wheel load (new, from C2).** Options: (a) restate R10 to allow about 75 N for the brief row-entry transient, subject to the module maker's frame guidance; (b) add a glass-height landing strip at the dock end so the brush is loaded on entry (small cost, over budget); (c) lower the preload to about 55 N and accept less traction. Recommendation: (a). **Decided by Amish, 2026-09-25: go with recommendation** (DRN-DDR-002, N2).
4. **Cost contingency (new, from I1).** The BOM uses the whole $500. Options: keep $500 and treat R13 as at risk until quotes exist; or raise `budget_usd` to about $550 to hold a 10 % contingency. Recommendation: keep $500 for now; decide on quotes. `budget_usd` is unchanged. **Decided by Amish, 2026-09-25: go with recommendation** (DRN-DDR-002, N3).

### Safety concerns

- Unattended rotating brush, belts and wheels that start on a timer: guards, a stop button on each truck, an audible start warning and a lockout at the dock. Stopping time is well inside 2 s on paper.
- A 13.8 kg robot falling from up to 1.6 m: end stops and the dock latch hold with factors over 4, but traction in wind along the row is marginal; the start wind limit (item 2) matters for safety as well as function.
- Live PV strings at several hundred volts DC: nothing on the robot may touch cables, connectors or junction boxes; damaged glass exposes live parts.
- LiFePO4 pack parked in the sun: BMS with low- and high-temperature charge cut-offs, fused output, sunshade and ventilation (R11 at risk).
- Hot glass and frames up to about 75 °C; module warranty risk from cleaning tools the maker has not cleared.

### Other notes

- No existing TRL 4 material was found (the `build-log/` folder holds only its README and was not touched).
- The review note listed no unchecked citations, so none were re-verified in this session.
- Friction coefficients, brush pile pressure and the visible frame flange width are assumptions; they drive R4, R9 and the brush power.

### Recommended next step

Decide items 2 to 4 above and name a pilot partner when ready. **TRL 4 is on hold by Amish's instruction**, and no TRL 4 work was started. For reference only, TRL 4 would need: measured friction of polyurethane on dusty frames and measured brush pile pressure and drag; a survey of target module frame profiles; a lab test article of one end truck on a frame section, and of the brush on sample glass (effectiveness and abrasion); a pack temperature check in the dock; a test report (TST, `environment: lab`) and build log entries.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now "Decided by Amish, 2026-09-25: go with recommendation", recorded in `docs/decisions/0002-recommendations-accepted.md` (DRN-DDR-002 v0.1).

### Decisions applied and what changed

| # | Decision | Before | After |
| --- | --- | --- | --- |
| N1 | Start a run only below 6 m/s at the dock anemometer; abort at 8 m/s | Operate below 8 m/s; traction margin 1.10 at start (friction 0.4) | Start below 6 m/s: margin 1.33 at friction 0.4, 1.00 at 0.3 [C13]; abort at 8 m/s: 1.10 and 0.82. R9 still at risk |
| N2 | R10 allows about 75 N per wheel for the row-entry transient | 72 N against a 60 N limit: R10 at risk | 72 N against 75 N (transient), 58 N against 60 N (steady): R10 met |
| N3 | Keep `budget_usd` at $500; decide contingency on quotes | $500, BOM $500.00 | Unchanged: $500, BOM $500.00; R13 still at risk |

Files changed: DRN-REQ-001 v0.3 to v0.4 (R9 and R10 restated, R13 note); DRN-PRC-001 v0.3 to v0.4 (start and abort rule, design choices, key numbers); DRN-CAL-001 v0.1 to v0.2 and `sizing.py` (new [C13], restated R9 and R10 checks); DRN-DDR-002 v0.1 (new); `project.yaml` (DDR-002 added to `trl_evidence`; `budget_usd`, pitch and problem unchanged); `README.md` (status line and the new write-up sections). Geometry, BOM and prices are unchanged, so DRN-DWG-001 stays at Rev P1; the STEP, STL, drawing, media and PDFs were regenerated.

### Requirement status now (DRN-CAL-001 v0.2)

| Status | Requirements |
| --- | --- |
| Not met | None |
| At risk | R4 (5 mm frame step and flange width); R9 (traction margin 1.33 at the 6 m/s start limit, 1.00 at friction 0.3); R11 (pack charge temperature in the sun); R13 ($500.00 against $500) |
| Not verifiable at TRL 3 | R2, R3, R6, R15 |
| Met | R1, R5, R7, R8, R10, R12, R14 |

Counts: 7 met (was 6), 4 at risk (was 5), 0 not met, 4 not verifiable.

### Still awaiting Amish

- O1: pilot site and co-design partner (no recommendation was made).

### Cross-repo actions

None. DustRunner uses its own 12.8 V pack (DRN-DDR-001, D6) and no shared module.

### TRL 4

TRL 4 remains on hold by Amish's instruction. The parts of N1 and N3 that need TRL 4 work (measuring wheel friction on dusty frames, writing firmware beyond a sketch, requesting supplier quotes) are decided but on hold. `trl: 3` and `trl_target: 3` are unchanged.

## Session 2026-09-26: sources strengthened

- "By country or region" in `README.md`: five of six rows had no citation. Each row now carries a verified primary or peer-reviewed source, and the text was trimmed to what the source supports:
  - Sahel and West Africa: no source, now [Isaacs et al., *Applied Energy*, 2023](https://www.sciencedirect.com/science/article/abs/pii/S0306261923003574) (Harmattan soiling losses above 50 % for decentralized solar; about 21 cleanings a year in Bamako).
  - India (Rajasthan, Gujarat): no source, now [Press Information Bureau, 8 February 2024](https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2004183&reg=3&lang=2) (PM-KUSUM off-grid solar pumps installed, national and Rajasthan figures).
  - Chile (Atacama): no source, now [Molina, Falvey and Rondanelli, *Scientific Reports*, 2017](https://www.nature.com/articles/s41598-017-13761-x) (highest long-term irradiance on Earth, very low cloud occurrence).
  - Australia (inland): no source, now [Geoscience Australia, deserts](https://www.ga.gov.au/scientific-topics/national-location-information/landforms/deserts); the unsupported claim about remote farms and service distances was removed.
  - US Southwest: removed, because no credible source was verified within this session's search allowance. Australia, Chile and Saudi Arabia remain as high-income examples.
- Arar figures (Alharbi, *Energies*, 2026): on checking the paper, the adopted monthly losses are about 4 % in winter rising to 15 % in June and July; 11 to 18 % is a literature range quoted for comparison. The README and DRN-PRB-001 (v0.4) now quote the adopted values, and the 60-day manual interval is stated as the base-case optimum, longer at low tariffs.
- Kept and verified: NASA InSight retirement release (What sparked the idea), Alharbi 2026. Ilse et al., *Joule*, 2019 is peer-reviewed and kept; it could not be re-fetched in this session.
- Not changed (outside this session's scope): DRN-PRB-001 still cites PV Tech (trade press) alone for the QEERI figures and Polywater (vendor) alone for water per module; both should get primary sources at the next revision.
- The "Qatar 11 to 18 %" wording in item 10 of the TRL 2 session above predates this correction.
- No budget change.
