---
doc_id: DRN-DEC-001
title: DustRunner design decisions register
project: DustRunner
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: Register opened with the build plan; open decisions from DRN-DDR-001 to 003 and the review note
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
---

# DustRunner design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, DRN-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Design for construction: accept the changes that make the design buildable (guide roller clevises and 28 mm plate gap, sprung hook sliders, flange bearings, drive housings, beam cleats, latch solenoid, dock rail brackets, frame clamps, vertical legs and mast, three-piece end stops) | Accept as drawn; or ask for changes | Accept | The whole build plan | DRN-DDR-003, P1 to P16 |
| 2 | Robot mass: 15.9 kg against R10's 15 kg, though every wheel load meets R10 | (a) restate R10's mass limit as 16.5 kg, keeping the 60 N and 75 N wheel-load limits; (b) save about 1 kg (4 mm or pocketed truck plates, 1.5 mm lower housing); (c) restate now and weigh at TRL 4 | (c) | Truck plates and housings if (b) | DRN-DDR-003, A2; DRN-CAL-001 [A3], [A4] |
| 3 | Payback: 3.2 years on a 60 m row at $573 (R14 not met; 3 years from about 64 m) | (a) restate R14 for rows of 65 m or more; (b) keep R14 and treat it as at risk until quotes; (c) relax it to 3.5 years on 60 m | (b), revisited once quotes exist | None | DRN-DDR-003, A3; DRN-CAL-001 [I4], [I9] |
| 4 | Latch release | (a) robot-side 12 V solenoid lifts its own pin, as drawn; (b) solenoid on the dock, switched through a fourth contact; (c) a passive latch the drives pull out of (parked wind case to recheck) | (a) | Contact bracket, solenoid, latch tab | DRN-DDR-003, A4 |
| 5 | Pilot site and co-design partner | A solar pumping farm, a mini-grid operator or a university test array | None yet (partners to be picked per area later) | Reference table and module frame for the first build | DRN-DDR-001 and 002, O1 |
| 6 | Product appearance model deviations 1 to 6 (render coordinates and layout, groups, small appearance parts, colours) | Accept; or change | Accept, then update the appearance model to the constructable design (item 7) | None (renders only) | `docs/REVIEW.md`, session 2026-09-26 |
| 7 | Photoreal renders, card and social preview now show the concept trucks, hook arms, dock legs and leaning mast | (a) update `cad/src/product_model.py` and re-render on Amish's Mac; (b) keep the concept renders and caption them as concept | (a) | None (renders only) | DRN-DDR-003, Consequences |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The target modules' frame: top flange at least 21 mm wide (25 mm assumed), frame 33 mm deep, and room on top of the long-side bottom flange for the 6 mm clamp jaw | Wheel tread, hook roller, dock rail profile and frame clamp all depend on it | DRN-CAL-001 [C12]; DRN-DDR-003, P12 |
| 2 | The flange bearings' bolt spacing and height (10 mm and 20 mm bores) | They set the bearing bolt holes and the clearances to the sensor brackets (4 mm) and clevises | DRN-DDR-003, P3, P5 |
| 3 | The gearmotors' face hole patterns and shaft sizes | They set the housing holes and the 6 to 10 mm coupling | DRN-DDR-003, P4 |
| 4 | A compression spring giving 60 N at 20 mm, about 9 mm across | Sets the hook preload | DRN-CAL-001 [C0] |
| 5 | The solenoid's pull and stroke against the pin's return spring, at 12 V for about 1 s | The robot must lift its own latch pin | DRN-DDR-003, P9 |
| 6 | The charge controller's LiFePO4 profile (14.4 V) and the pack BMS's 0 °C and 45 °C charge cut-offs | Battery safety (R11) | DRN-PRC-001, Safety |
| 7 | The module maker's cleaning and frame-load guidance (60 N steady, 75 N at row entry) | R3 and R10 | DRN-DDR-002, N2 |
| 8 | The real masses of the bought parts | The 15.9 kg estimate and the preload rule | DRN-CAL-001 [A2], [A4] |

## Value engineering

Value-engineering target: USD 500 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 573 (USD 73 over the target). Main cost drivers and savings worth trying:

- The USD 73 over the target is the parts added to make the design buildable (DRN-DDR-003): flange bearings, drive housings, couplings, roller clevises and sliders, dock brackets, clamps, ties and foot plates, the latch solenoid and beam cleats. The largest single lines are the LiFePO4 pack (USD 45), the beam (USD 30) and the dock panel (USD 22).
- Savings worth trying at quotes: cheaper flange bearings, a lighter dock, and 4 mm or pocketed truck plates (which also save about 1 kg, item 2 above).
- Every price is indicative; quotes are TRL 4 work and on hold (DRN-DDR-002, N3).

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D12: full-width robot on 1P frames, evening cleaning gated by humidity, dock anemometer, 20 W dock charging, both wheels driven with preloaded hook rollers, 12.8 V LiFePO4 pack, 40 m reference row, R14 restated for rows of 60 m or more, budget $500, 1P portrait 2,278 mm modules first, mechanical end stops kept, dry microfiber without airflow | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | DRN-DDR-001 |
| 2026-09-25 | Start a run only below 6 m/s and abort at 8 m/s (N1); R10 allows 75 N per wheel for the row-entry transient (N2); keep `budget_usd` at $500 as the value-engineering target and look at contingency on quotes (N3) | Amish: "i accept all your recommendations, go with them across all repos." | DRN-DDR-002 |
| 2026-09-26 | DustRunner chosen for the first batch of product renders | Amish | `docs/REVIEW.md`, session 2026-09-26 |
| 2026-09-30 | Write the illustrated build plan and make the design physically buildable while drawing it; keep open decisions out of the build plan, in this register | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The changes made under this instruction are open for his review (open item 1). | DRN-DDR-003; DRN-BLD-001 |
