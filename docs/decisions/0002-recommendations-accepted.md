---
doc_id: DRN-DDR-002
title: DustRunner recommendations accepted
project: DustRunner
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of the TRL 3 review recommendations and the items that remain open
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted for items N1 to N3; item O1 remains proposed

## Context

The TRL 3 review note (`docs/REVIEW.md`, session 2026-09-25, TRL 3) listed four items as "Proposed, awaiting Amish". Three came from the calculations in DRN-CAL-001 v0.1 and each carried a recommendation; the fourth, the pilot site and co-design partner, carried none. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is therefore decided in favor of that recommendation. The item without one stays open. The TRL 2 items were already decided in DRN-DDR-001 (D1 to D12).

TRL 4 (building, testing, measuring, purchasing) remains on hold by Amish's instruction, so any part of a decision that needs TRL 4 work is recorded as decided but on hold.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, TRL 3, "Proposed, awaiting Amish", items 2 to 4).

## Decision

*Table 1. Newly decided items.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| N1 | Start wind limit (R9) | Option (b): start a run only below 6 m/s at the dock anemometer and keep 8 m/s as the abort limit; revisit once friction is measured. Decided by Amish, 2026-09-25: go with recommendation. | R9 target restated in DRN-REQ-001 v0.4. Firmware rule described in DRN-PRC-001 v0.4. DRN-CAL-001 v0.2 adds [C13]: traction margin 1.33 at 6 m/s (friction 0.4), up from 1.10 at 8 m/s; 1.00 at friction 0.3. R9 stays at risk. The friction measurement is TRL 4 and on hold. |
| N2 | Row-entry wheel load (R10) | Option (a): restate R10 to allow about 75 N per wheel for the brief row-entry transient, subject to the module maker's frame guidance; no landing strip, preload unchanged at 70 N. Decided by Amish, 2026-09-25: go with recommendation. | R10 target restated in DRN-REQ-001 v0.4 (60 N steady, 75 N transient). The 72 N transient [C2] now meets it: R10 moves from at risk to met on paper. No geometry change. |
| N3 | Cost contingency (R13) | Keep `budget_usd` at $500 for now and decide on a contingency once quotes exist. Decided by Amish, 2026-09-25: go with recommendation. | `budget_usd` unchanged at $500. R13 stays at risk ($500.00 against $500). Requesting quotes is purchasing, TRL 4 work, and on hold. |

*Table 2. Item that remains open (no recommendation was made).*

| # | Item | Status |
| --- | --- | --- |
| O1 | Pilot site and co-design partner: a solar pumping farm, a mini-grid operator or a university test array | Proposed, awaiting Amish |

## Consequences

- Requirement status (DRN-CAL-001 v0.2, Table 8): 7 met, 4 at risk (R4, R9, R11, R13), 0 not met, 4 not verifiable at TRL 3 (R2, R3, R6, R15). Before: 6 met, 5 at risk.
- DRN-REQ-001, DRN-PRC-001 and DRN-CAL-001 are each revised by one minor version. `docs/04-calcs/sizing.py` gains the start limit and the restated R9 and R10 checks.
- The model, BOM and drawing DRN-DWG-001 are unchanged in geometry and price; the drawing stays at Rev P1 and was re-rendered.
- No cross-repo actions arise: DustRunner uses its own pack and no shared module.
- TRL stays at 3. Nothing in this record authorizes building, testing or purchasing.
