---
title: Early Filter and Cache
description: 'When writing KQL (hunting queries or ASIM parsers), optimize for fewer
  rows and fewer expensive computations:


  1) Prefilter early (before parse/branch work)'
repository: Azure/Azure-Sentinel
label: Performance Optimization
language: Yaml
comments_count: 7
repository_stars: 6042
---

When writing KQL (hunting queries or ASIM parsers), optimize for fewer rows and fewer expensive computations:

1) Prefilter early (before parse/branch work)
- Apply vendor/product/event-id filters and any simple parameter filters as close to the source table as possible.
- Avoid “post-filtering” after heavy parsing/union/branching. If a filter can’t be applied globally, it must be applied inside each branch (so you don’t effectively re-filter the same data multiple times).

2) Materialize reused datasets
- If you deduplicate or aggregate the same high-volume table more than once, compute it once and reuse it (e.g., Latest = materialize(...)).

3) Cache expensive expressions
- If you call costly functions repeatedly (e.g., todynamic(collection_arr), multiple split/extract/regex operations), compute once into a let/extend variable, then reference it.
- If a field is equivalent to another derived value, alias instead of recomputing.

4) Keep dedup correct and efficient
- Be careful with arg_max(*)-style wide projections; if dedup requires the whole winning row, ensure the “winner” selection is correct while minimizing unnecessary wide operations.

Example pattern
```kql
let LatestAgents = materialize(
    AgentsInfo
    | summarize arg_max(Timestamp, *) by AgentId
    | where LifecycleStatus != "Deleted"
);

let AgentToolNames = LatestAgents
| where array_length(DeclaredTools) > 0
| mv-expand Tool = DeclaredTools
| extend ToolName = tostring(Tool.name)
| where isnotempty(ToolName)
| summarize ToolNames = make_set(ToolName) by AgentId;

LatestAgents
| join kind=leftouter AgentToolNames on AgentId
```

Checklist
- Can any filter be moved earlier (before parse-kv, mv-apply, lookup/union branches)?
- Is any large subquery scanned twice? If yes, materialize it.
- Are any expensive expressions computed multiple times? If yes, compute once and reuse/alias.