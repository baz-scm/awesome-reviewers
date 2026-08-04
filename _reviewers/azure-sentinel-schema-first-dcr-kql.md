---
title: Schema-First DCR KQL
description: 'For data connector definitions (DCR + KQL transforms), treat the DCR
  `streamDeclarations.columns` as the schema contract and ensure KQL transforms match
  that contract:'
repository: Azure/Azure-Sentinel
label: Database
language: Json
comments_count: 6
repository_stars: 6042
---

For data connector definitions (DCR + KQL transforms), treat the DCR `streamDeclarations.columns` as the schema contract and ensure KQL transforms match that contract:

- **Map fields that truly exist**: if the source/transform doesn’t return `TimeGenerated`, don’t declare/use it in the DCR; instead map it in KQL from the correct source timestamp.
- **Match types exactly**: if a column is `dynamic` in the DCR (e.g., list fields like `DetectionList`), don’t coerce it with `tostring(...)` in KQL—keep it as `dynamic` (or map it consistently with the declared type).
- **Use the DCR-shaped columns**: if DCR stores payload parts as JSON strings, avoid dot-access; use the DCR-flattened columns produced by the transform (e.g., `abx_metadata_event_type_s`, `abx_body_...`).
- **Prefer explicit column selection**: avoid `project-away` when it can break table creation/downstream expectations. Use `project <explicit column list>` (and/or explicit `arg_max(...)` column lists) so the resulting schema is deterministic.

Example pattern (explicit + type-aligned):
```kusto
source
| extend
    EventTimestamp = todatetime(created_at),
    // keep dynamic/list fields as-is if DCR declares dynamic
    DetectionListDyn = DETECTION_LIST
| project
    TimeGenerated = EventTimestamp,
    DetectionList = DetectionListDyn,
    // add only stable columns you declare in the DCR
    HostId, IPAddress, TrackingMethod, OperatingSystem
```