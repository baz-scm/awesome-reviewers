---
title: Prefer Explicit Projection
description: 'When normalizing/querying, keep output schemas deterministic and readable:


  - Prefer explicit output selection (`project` / `project-keep`) over `project-away`,
  so adding new columns later won’t accidentally change results.'
repository: Azure/Azure-Sentinel
label: Code Style
language: Yaml
comments_count: 3
repository_stars: 6042
---

When normalizing/querying, keep output schemas deterministic and readable:

- Prefer explicit output selection (`project` / `project-keep`) over `project-away`, so adding new columns later won’t accidentally change results.
- Consolidate related `extend` operations into fewer, clearer steps; remove redundant helper columns that don’t affect the final output.
- Avoid brittle fixed-position array access (e.g., `TargetResources[0]`); use parsing/`where`/structured extraction so logic doesn’t depend on unreliable ordering.

Example (avoid `project-away`):
```kusto
// Prefer explicit projection
... 
| project
    TimeGenerated,
    EventUid,
    DvcIpAddr,
    EventSchema,
    EventSchemaVersion,
    EventMessage,
    AdditionalFields
// (Do not rely on project-away for final output stability)
```

Example (combine extends):
```kusto
... 
| extend timestamp=TimeGenerated,
         HostName = tostring(split(DeviceName, '.', 0)[0]),
         DnsDomain = tostring(strcat_array(array_slice(split(DeviceName, '.'), 1, -1), '.'))
``` 

Example (avoid positional indexing):
- Replace `TargetResources[0]`-style access with parsing/filters that locate the correct element by key/value rather than index.