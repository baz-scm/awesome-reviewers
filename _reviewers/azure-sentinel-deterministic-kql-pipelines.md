---
title: Deterministic KQL Pipelines
description: 'Treat each analytics/hunting query as a deterministic algorithm: parse
  based on the actual encoded input, collapse repeated events by key, and use correct
  expand/join/re-aggregate patterns so results are complete and non-duplicative.'
repository: Azure/Azure-Sentinel
label: Algorithms
language: Yaml
comments_count: 5
repository_stars: 6042
---

Treat each analytics/hunting query as a deterministic algorithm: parse based on the actual encoded input, collapse repeated events by key, and use correct expand/join/re-aggregate patterns so results are complete and non-duplicative.

**Standards**
1) **Validate parsing assumptions before changing algorithms**
- If a field is stored as an ingestion-produced JSON-encoded string, prefer `parse_json()` over `split()`.
- Don’t “blindly” switch parsing when the true on-disk shape isn’t confirmed.

2) **Collapse duplicates by the real business key**
- If upstream can emit multiple events per case/alert, dedupe deterministically:
  - `summarize arg_min(TimeGenerated, *) by CaseId` (or the equivalent key)

3) **For 1-to-many relationships, preserve completeness**
- Use `mv-expand` (or equivalent) to expand arrays, `join` to map IDs to details, then re-aggregate with `make_set()`.

4) **Filtering parsers should be strict**
- If required filter specs can’t be met, returning zero rows is the correct behavior; avoid fuzzy partial matches.

**Example pattern (dedupe + deterministic projection)**
```kql
MyAlertTable
| where isnotempty(CaseId)
| summarize arg_min(TimeGenerated, *) by CaseId
| project TimeGenerated, CaseId, /* other fields */
```

**Example pattern (expand→join→re-aggregate)**
```kql
IdentityEnabled
| where IsAccountEnabled == 1
| distinct AccountObjectId = tostring(AccountObjectId)
| join kind=leftanti (
    AgentsInfo
    | summarize arg_max(Timestamp, *) by AgentId
    | mv-expand Owner = Owners to typeof(string)
    | extend OwnerId = tostring(Owner)
    | where isnotempty(OwnerId)
) on $left.AccountObjectId == $right.OwnerId
// (then join OwnerId->UPN and make_set() in the final projection)
```

Applying this standard reduces regression risk from parsing changes, prevents duplicate incidents/alerts, and ensures relationship-based logic (arrays of owners/targets) produces correct, complete outputs.