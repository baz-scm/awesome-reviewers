---
title: Stable, Scoped Query Outputs
description: "When writing KQL for Sentinel (parsers, analytic rules, hunts), make\
  \ query outputs and intermediate datasets stable and correct: \n\n- Prefer **explicit\
  \ `project`** of the expected/normalized columns (avoid `project-away`) so newly\
  \ added source columns won’t change the published schema."
repository: Azure/Azure-Sentinel
label: Database
language: Yaml
comments_count: 7
repository_stars: 6042
---

When writing KQL for Sentinel (parsers, analytic rules, hunts), make query outputs and intermediate datasets stable and correct: 

- Prefer **explicit `project`** of the expected/normalized columns (avoid `project-away`) so newly added source columns won’t change the published schema.
- Apply **required scoping and data-quality filters** *before* `arg_max`/`summarize` (e.g., vendor scoping, excluding deleted/baseline-invalid records).
- Ensure **deduplication via `summarize`** on the intended entity key (e.g., `SrcIpAddr`) so you don’t emit duplicate entities.
- Guard against **schema drift across connector versions** by unioning V2/V3 tables when fields move.

Example patterns:

```kql
// 1) Stable output schema (no project-away)
SourceTable
| where DeviceVendor =~ "Ubiquiti"
| summarize count() by SrcIpAddr
| project  // explicitly list the final ASIM/expected columns
    TimeGenerated,
    EventType,
    SrcIpAddr,
    DeviceVendor;

// 2) Version drift handling
union isfuzzy=true
    SalesforceServiceCloudV2_CL,
    SalesforceServiceCloudV3_CL
| ...;

// 3) Baseline correctness before arg_max
BaselineTable
| where LifecycleStatus != "Deleted"
| summarize arg_max(Timestamp, *) by AgentId
| ...;
```

Adopting this standard reduces silent schema changes, incorrect baseline/detection logic, and duplicate or mis-resolved entities.