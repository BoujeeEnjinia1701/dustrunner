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

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26.

### What was done

- `cad/src/product_model.py` (new): a product appearance model for photoreal renders. `product_parts()` returns every part with its colour, material, BOM line, group and exploded-view offset; `TITLE` and `RENDER_VIEWS` define three views: `hero` (robot partway along a two-module row with its dock and anemometer in front), `exploded` (robot, dock and end stops) and `detail` (the lower end truck clamped on a section of the module frame). It adds:
  - Robot: anodized beam with fillets, an accent stripe and a name plate; white powder-coated hood with rolled edges, hangers and an accent band; microfiber sleeve (fabric) on its core ends, stub shafts and bearing flanges; sunshade frame on four posts; strapped LiFePO4 pack with a label; IP65 controller box with a lid parting line, a clear side window showing the board, a shielded module and a lit status light, a main switch and cable glands.
  - End trucks: graphite plates with corner fillets, lightening holes, bolts and a badge; polyurethane tyres on metal hubs; wheel belt guards; drive gearmotors split into gearbox, can and encoder cap; guide rollers on clevis tabs; hook arms with rollers and preload springs; IR sensors with lenses; copper charge contacts; a red emergency stop on a yellow base on each truck (the two stop buttons of BOM item 15). The lower truck also carries the brush gearmotor housing (with cooling slots) and the brush belt cover.
  - Dock: C-section rails, cross members and posts, painted clamps with bolts, legs with feet, a framed 20 W panel with cells, a charger box with a lit charge light, spring contacts with the latch pin on a contact post, and a three-cup anemometer on its mast. End stops get rubber buffers and clamp bolts.
  - Context (not in the BOM): two reference modules (frames, backsheet, cells), a dust film ahead of the robot (illustrative), purlins, rafters, posts with concrete footings and a compact gravel ground patch.
- `README.md`: the hero image now points to `media/render-hero.png`, and the links line starts with the exploded render. The render files will be produced by the orchestrator.
- Self-check previews (matplotlib, clear parts left out) were reviewed for all three views; they are scratch files, not repo media.

### Differences from model.py (each Proposed, awaiting Amish)

1. Coordinates. model.py builds everything in local table coordinates (glass plane). The product model builds each part in those coordinates and then places it with the same tilt transform as `cad/src/concept_media.py` (Z up, ground at Z = 0), because the renderer needs a ground plane. Recommendation: accept; no dimension changes.
2. Scene layout. The robot is shown at u = 560 mm, partway along the first of two modules, not parked in the dock as in `assembly()`. Recommendation: accept, since it shows the brush on the glass and the dock together.
3. Exploded view. The dock is drawn 300 mm nearer the robot along the row and the end stops 900 mm nearer, so the exploded view stays compact; the dock legs are left out of it. Recommendation: accept (render layout only).
4. Groups. The lower end truck, the brush drive and a short section of the module frame are in the `internal` group so the `detail` view can frame the edge clamp; the upper truck, its mirror image, is in `shell`. Recommendation: accept.
5. Small appearance additions not in model.py: a bracket and foot that tie the dock contact block to the rail (model.py shows the block alone), the sunshade posts and cross bars that seat it on the beam, bearing flanges on the truck plates, hood hangers, pack straps, and rubber buffers on the end stops. These imply small hardware covered by BOM items 3, 11, 13, 14 and 15; no BOM line or cost changes. Recommendation: accept as appearance only, and confirm the dock contact bracket at the next design revision.
6. Materials and colours. Wheel tyres are shown in the kit accent (#0F766E) and the hood and sunshade in white powder coat; model.py sets no finishes. Recommendation: accept, or choose a different tyre colour.

### Status

This is an appearance model only: no tolerances, no fabrication detail, no change to PARAMS, the BOM, the calculations or the drawing. `trl` stays 3 and TRL 4 remains on hold.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-09-30: prototype build plan and design for construction (kit 1.7.0)

Kit 1.7.0 installed (`.kit/`, `.claude/commands/`, `CLAUDE.md`). Amish's instructions of 2026-09-30: write the illustrated build plan in the approved format, "fix the design assumptions to match and be physically feasible as you draw the illustrations", and keep outstanding decisions out of the build plan in a separate register.

### What was done

- `cad/src/model.py` rebuilt to a constructable level of detail: `build_components()` returns every robot, dock and end-stop part; `python cad/src/model.py --check` runs 123 constructability checks (contacts, clearances, robot on the module, parked in the dock and at the end stop, hook roller path); all 123 pass. STEP and STL re-exported.
- `docs/decisions/0003-design-for-construction.md` (DRN-DDR-003 v0.1, Draft): every change, its reason, the knock-on changes and four items proposed, awaiting Amish.
- `docs/05-build-plan.md` (DRN-BLD-001 v0.1): 19 made components, bought parts, wiring, 15 assembly steps, first checks, safety stops, tools.
- `docs/06-design-decisions.md` (DRN-DEC-001 v0.1): 8 open decisions (7 after the 2026-10-01 budget wording pass), 8 items to confirm when parts are bought, decisions made.
- `cad/src/build_plan_media.py`: overview pictures (robot and dock), making sketches `cad/drawings/DRN-DWG-101` to `119`, 11 joint close-ups, 15 step pictures and a wiring diagram in `docs/05-build-plan/`.
- `docs/04-calcs/sizing.py` and DRN-CAL-001 v0.3 re-run for the constructable design (new [A4], [C0], [I9]); DRN-REQ-001 v0.5 and DRN-PRC-001 v0.5 updated; `bom/bom.csv` and `bom/bom-notes.md` repriced; `cad/src/sheets.py` and DRN-DWG-001 Rev P3; concept media regenerated (`cad/src/concept_media.py`); `project.yaml` (`design_state: constructable`, new evidence); README links line, "Building the prototype" and a short "Safety" section.

### Design changes made for construction (DRN-DDR-003)

1. Truck plate gap 28 mm (was 22): each guide roller now turns on an M8 bolt in a folded clevis, 6 mm off the plate (it used to fill the gap and rub the plate).
2. Hook roller on an 8 mm axle cantilevered from a 10 mm slider that runs on shoulder bolts and is pushed up by a spring on a seat bracket (the concept had a rigid arm, no axle, no spring); plates 24 mm taller (296 mm).
3. Each wheel axle in two flange bearings, one each side of the plate (stub axles could not carry the outboard belt).
4. Folded drive housings on the outer faces guard the belts and carry the gearmotors (which floated); shaft couplings; wheel and brush belts in separate layers; lower brush shaft stepped to 15 mm outboard of the plate.
5. Turned core end plugs, stub shafts in the plugs, and a 20 mm flange bearing on each plate (shafts butted the core and passed through the plates with no bearing).
6. Beam bolted to each plate by two angle cleats (it butted, unfixed).
7. Hood hung on five 3 mm spacers; sunshade on four posts; pack strapped (all floated).
8. IR sensors and the robot contact block on folded brackets on the plate face (they butted the plate edge).
9. Dock latch made real: a 12 V spring-return solenoid on the robot drops its 6 mm pin through a latch tab on the dock.
10. Dock contact block on a post bolted to the rail-start cross member (it floated 89 mm above the frame).
11. Dock cross members moved 6 mm below the rails and 30 mm inside them, rails held by L brackets inside the channel with spacers and shims; the two posts that blocked the hook roller's path removed.
12. Frame clamps rebuilt as bar, jaw, spacer and one M8 bolt round the first module's bottom flange (they touched nothing).
13. Dock legs vertical, bolted beside the cross members, on foot plates; three ties added; vertical anemometer mast in U-bolt clamps (it leaned 25°).
14. End stops rebuilt as three screwed pieces with an M8 clamp screw, 40 mm tall so the IR sensors pass over and the wheels meet the buffer (a sensor used to hit the stop first).
15. Reference module long sides modelled as C sections (context only).

### Key results (DRN-CAL-001 v0.3)

- Robot 15.9 kg (was 13.8 kg; about 2.1 kg of construction parts). Hook preload 60 N per truck by the existing 60 N wheel-load rule (was 70 N); wheel loads 56 N brushing, 59 N worst tilt, 73 N at row entry; traction margin 1.30 at the 6 m/s start limit (0.98 at friction 0.3).
- Parts $573.00 (was $500.00), USD 73 over the $500 value-engineering target. Payback 3.2 years on a 60 m row; 3 years from 63.5 m.
- Requirements: 5 met, 3 at risk (R4, R9, R11), **3 short of target: R10 (mass; wheel loads met), R13 (over the value-engineering target by USD 73: $573 against $500), R14 (3.2 years on 60 m)**, 4 not verifiable at TRL 3.

### Proposed, awaiting Amish

See DRN-DEC-001, open items 1 to 7: accept DRN-DDR-003 (recommend accept); restate R10's mass limit to 16.5 kg and weigh at TRL 4; keep R14 at risk until quotes; robot-side latch solenoid; pilot partner (no recommendation); render deviations of 2026-09-26; update the appearance model and renders. The budget is no longer an open decision: `budget_usd` stays $500 as a value-engineering target, and the savings worth trying are in the register's Value engineering section (2026-10-01).

### Stale media

The design changed visibly, so `media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png`, `media/social-preview.png` and `cad/src/product_model.py` are stale (concept trucks, hook arms, dock legs, leaning mast). They are made on Amish's Mac and were not regenerated.

### Safety concerns

- The latch now depends on a solenoid on the robot; it fails latched (spring out), and the parked-wind check [D2] is unchanged.
- The drive housings fully enclose the wheel and brush belts (pinch points, R12); the stop buttons sit in the truck plates.
- The dock must be clamped to the module frame without drilling and kept clear of array cables and junction boxes (build plan S5).

### Recommended next step

Amish reviews DRN-DDR-003 and the register, and decides the budget, R10 and R14 items. TRL 4 stays on hold; the build plan is paper only.

## Session 2026-10-02: open decisions decided

Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This approves the recommendation written for each open decision in the design decisions register (DRN-DEC-001 v0.2). trl stays 3; no build or test work was done, and the model, BOM quantities and prices, and pictures are unchanged.

### Decisions recorded

Seven decisions, all moved to Decisions made in DRN-DEC-001, dated 2026-10-02:

1. DRN-DDR-003 accepted: design-for-construction changes P1 to P16, as drawn.
2. Robot mass: option (c), R10's mass limit restated as 16.5 kg, the 60 N and 75 N wheel-load limits unchanged; the robot is weighed at TRL 4.
3. Payback: option (b), R14 kept at 3 years on 60 m rows and marked at risk; revisited when real quotes exist.
4. Latch release: option (a), the robot-side 12 V solenoid lifts its own pin.
5. Pilot site and co-design partner: a university or national lab outdoor PV test site in a dusty climate; Arizona State University's Photovoltaic Reliability Laboratory in Mesa is the first candidate to approach.
6. Appearance items 1 to 6 accepted for renders, except that the dock contact bracket and bearing flanges (item 5) come from the constructable design, not as appearance-only parts.
7. Renders: option (a), update the appearance model to the constructable design and re-render on Amish's Mac.

Requirement status after decisions 2 and 3: 6 met on paper (R10 now met at 15.9 kg against 16.5 kg), 4 at risk (R4, R9, R11 and R14), 1 short of target (R13, USD 73 over the value-engineering target), 4 not verifiable at TRL 3.

### Documents changed

- `docs/06-design-decisions.md` (DRN-DEC-001 v0.3): open decisions moved to Decisions made; the truck-plate saving and the 2026-09-30 row updated.
- `docs/decisions/0003-design-for-construction.md` (DRN-DDR-003 v0.3, status Draft): accepted, with A2 to A4 accepted as recommended and a consequence added.
- `docs/decisions/0001-trl2-review-decisions.md` (DRN-DDR-001 v0.2) and `docs/decisions/0002-recommendations-accepted.md` (DRN-DDR-002 v0.2): O1 recorded as decided.
- `docs/03-requirements.md` (DRN-REQ-001 v0.7): R10 restated to 16.5 kg (met on paper); R14 at risk; summary counts.
- `docs/04-calcs/01-sizing.md` (DRN-CAL-001 v0.5): requirement table status for R10 and R14, counts and summary; no number re-run.
- `docs/02-concept.md` (DRN-PRC-001 v0.7): key numbers status for R10 and R14; pilot site question answered.
- `docs/01-problem.md` (DRN-PRB-001 v0.5): pilot site question answered.
- `README.md`: requirement summary.

### Follow-up actions to carry approved decisions into the design

1. Decision 2 (calculations): change R10's mass limit to 16.5 kg in `docs/04-calcs/sizing.py` so that its status line [J0] prints the decided counts.
2. Decision 3 (calculations): print R14 as at risk in `sizing.py` [J0], and recheck payback when real quotes exist.
3. Decision 6 (model): build the dock contact bracket and the bearing flanges in `cad/src/product_model.py` from the constructable parts of `cad/src/model.py`, not as appearance-only parts.
4. Decision 7 (pictures): update `cad/src/product_model.py` to the constructable design (trucks, hook arms, dock legs, vertical mast) and re-render the photoreal renders, `media/card.png` and `media/social-preview.png` on Amish's Mac.

### Points found in the review

- The row length at which payback reaches 3 years is given three ways: 63.5 m (DRN-DDR-003 and R14), about 64 m (the register's former item 3 and the README) and 65 m (option a).
- R14 was marked "Not met" in the requirements while the recommendation was to treat it as at risk; aligned now that item 3 is decided.

## Approved follow-ups carried out (2026-10-02)

Amish approved all follow-up actions from the 2026-10-02 sign-off. trl stays 3; no build or test work was done. No decision changed the geometry or the BOM, so `cad/src/model.py`, STEP, STL, `bom/bom.csv` and all build plan and concept pictures are unchanged.

### Follow-ups

1. Decision 2 (calculations): done. `docs/04-calcs/sizing.py` tests R10 against 16.5 kg (restated 2026-10-02); R10 is met at 15.9 kg.
2. Decision 3 (calculations): done. `sizing.py` prints R14 as at risk (3.2 years on a 60 m row against the 3 years kept; met from 63.5 m); payback is to be rechecked when real quotes exist (TRL 4 work, not done here). The cost line [I1] now uses the value-engineering wording: "Value-engineering target: USD 500. Estimated cost of the constructable design: USD 573 (USD 73 over the target)". R13 prints as "Short of target". The printed counts [J0] now agree with the decided counts: 6 met, 4 at risk, 1 short of target, 4 not verifiable at TRL 3.
3. Decision 6 (model): done. The dock contact bracket, the dock contact post and block, the latch solenoid and tab, and the flange bearings (axle and brush) in `cad/src/product_model.py` are now model.py's own parts, not appearance-only parts.
4. Decision 7 (appearance model and pictures): done in part. `cad/src/product_model.py` now takes both end trucks (plates, drive housings, clevis-mounted guide rollers, sprung hook sliders, beam cleats, sensor brackets), the beam cleat holes, hood spacers, sunshade posts and pack straps, the dock (rails on brackets, cross members, clamps, ties, vertical legs on foot plates, panel on the ties, charger, contact post) and the vertical mast with its clamps and the three-piece end stops from the constructable model. Render scenes were exported to `/home/claude/renders/dustrunner` (hero, exploded, detail, and the jobs file). Not done: the photoreal renders, `media/card.png` and `media/social-preview.png`, which are made on Amish's Mac.

### Key results

- Cost: USD 573 against the USD 500 value-engineering target (USD 73 over); unchanged. Mass: robot 15.9 kg; unchanged. `budget_usd` is unchanged.
- Requirement status changes: none in the documents (the script now prints the decided status). 6 met, 4 at risk (R4, R9, R11, R14), 1 short of target (R13), 4 not verifiable at TRL 3.
- Appearance deviations from model.py: the truck plate has no lightening holes (they would clash with the bolts of the constructable truck), and the anemometer cups, panel cells and charger label are appearance detail. Recorded as accepted by decision 6 of 2026-10-02; nothing new is proposed.

### Documents changed

- `docs/04-calcs/01-sizing.md` (DRN-CAL-001 v0.6), `docs/03-requirements.md` (DRN-REQ-001 v0.8), `docs/02-concept.md` (DRN-PRC-001 v0.8), `docs/05-build-plan.md` (DRN-BLD-001 v0.3, Rev P4 reference), `docs/decisions/0003-design-for-construction.md` (DRN-DDR-003 v0.4).
- `cad/src/sheets.py` and `cad/drawings/DRN-DWG-001` at Rev P4 (no geometry change); `cad/src/product_model.py`; `docs/04-calcs/sizing.py`.
- PDFs re-rendered with `python3 .kit/render.py`.

### Cross-repo actions

None.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.
