---
doc_id: DRN-DDR-001
title: DustRunner TRL 2 review decisions
project: DustRunner
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions on the TRL 2 review items and the items that remain open
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: O1 decided by Amish on 2026-10-02 as recommended (ASU Photovoltaic Reliability Laboratory as first candidate pilot site)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for items D1 to D12; item O1 decided on 2026-10-02 as recommended (Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions.")

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed ten items as "Proposed, awaiting Amish", and the design precis DRN-PRC-001 v0.2 and problem statement DRN-PRB-001 v0.2 listed further design choices and open questions, each with options. On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided in favor of that recommendation. Items without a recommendation stay open.

The same instruction approved three portfolio-wide decisions: SwapCell interface v0.3 adds a wake method for hosts without CAN, a charge-while-discharging mode and a latch vibration rating for vehicles; shared SwapCell packs are priced once and excluded from each dependent kit budget; and community designs pick co-design partners per area later. DustRunner does not use a SwapCell pack (D6), so the first two do not change this design.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate), in DRN-PRC-001 v0.2 (Key design choices) and in DRN-PRB-001 v0.2 (Open questions).

## Decision

*Table 1. Decided items.*

| # | Item | Decision |
| --- | --- | --- |
| D1 | Scope | Option (a): one full-width robot per row, riding on the module frames of 1P portrait tables, rather than a smaller robot on the glass or a transfer cart between rows. The fit limit (short module edges free of clamps) stays in R4. Decided by Amish, 2026-09-25: go with recommendation. |
| D2 | Cleaning time | In the evening, after the array's output has dropped and before dew forms, gated by the humidity sensor; not at night or at dawn. Decided by Amish, 2026-09-25: go with recommendation. |
| D3 | Wind input | Option (a): a cup anemometer at the dock (about $15), not a weather feed or a motor-current rule alone. It is BOM item 16. Decided by Amish, 2026-09-25: go with recommendation. |
| D4 | Charging | A 20 W panel at the dock charging the parked robot through spring contacts, not a panel on the robot. Decided by Amish, 2026-09-25: go with recommendation. |
| D5 | Traction | Both wheels driven on each end truck (belt-linked) and spring-preloaded hook rollers under the frame lip, pending a friction measurement. Decided by Amish, 2026-09-25: go with recommendation. |
| D6 | Battery | A 12.8 V 10 Ah LiFePO4 pack with BMS; no SwapCell pack, because DustRunner needs about a quarter of a SwapCell's energy at a quarter of its voltage. Decided by Amish, 2026-09-25: go with recommendation. |
| D7 | Reference row | Keep the 40 m, 20 kWp reference row (35 modules) for the requirements and the design case. Decided by Amish, 2026-09-25: go with recommendation. |
| D8 | R14 target | Restate R14 as "payback of 3 years or less on rows of 60 m or more", mid case, rather than keeping 3 years on the 40 m row or relaxing it to 5 years. Decided by Amish, 2026-09-25: go with recommendation. |
| D9 | Budget and wording | Keep `budget_usd` at $500 for one robot and its dock, now including the anemometer. Keep the pitch. Reword the problem line to "up to 15 to 25% a month in the dusty season" in `project.yaml` and `README.md`. Decided by Amish, 2026-09-25: go with recommendation. |
| D10 | First table format | 1P portrait tables of 2,278 mm modules with 30 to 35 mm frames. Decided by Amish, 2026-09-25: go with recommendation. |
| D11 | End stops | Keep clamp-on mechanical end stops as the independent backstop to the IR sensors (R9). Decided by Amish, 2026-09-25: go with recommendation. |
| D12 | Cleaning medium | A dry microfiber brush, with no water and no airflow stage; add airflow only if tests show that dust is re-deposited. Decided by Amish, 2026-09-25: go with recommendation. |

*Table 2. Item that remains open (no recommendation was made).*

| # | Item | Status |
| --- | --- | --- |
| O1 | Pilot site and co-design partner: a solar pumping farm, a mini-grid operator or a university test array | Decided by Amish on 2026-10-02 as recommended in DRN-DEC-001: a university or national lab outdoor PV test site in a dusty climate, with Arizona State University's Photovoltaic Reliability Laboratory in Mesa as the first candidate to approach |

## Consequences

- `project.yaml` and `README.md`: the problem line reads "Soiling cuts output of PV arrays in dusty regions by up to 15 to 25% a month in the dusty season, and water for washing is scarce." The pitch and `budget_usd` ($500) are unchanged.
- DRN-PRB-001, DRN-PRC-001 and DRN-REQ-001 are revised to v0.3. R14 is restated per D8; R13 keeps $500 and now covers the robot, the dock and the anemometer. The key design choices in the precis are no longer "proposed".
- The BOM gains item 16 (dock anemometer, $15), which brings the indicative total to exactly $500 (DRN-CAL-001, I1), so R13 has no margin.
- The TRL 3 calculations (DRN-CAL-001) raise new questions about the operating wind limit, the wheel load at row entry and the budget margin. They are listed in `docs/REVIEW.md` as "Proposed, awaiting Amish"; this record does not decide them.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
