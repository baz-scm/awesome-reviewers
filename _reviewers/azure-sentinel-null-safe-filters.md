---
title: Null-safe Filters
description: Ensure queries and ASIM parsers handle nullable/optional fields safely
  by (1) using type-correct null checks, (2) guarding references to optional/missing
  columns with `column_ifexists` (and using the same guarded form in both `summarize`
  and `project`), and (3) gating filters/fields that the source cannot provide so
  they don’t unintentionally exclude all...
repository: Azure/Azure-Sentinel
label: Null Handling
language: Yaml
comments_count: 12
repository_stars: 6042
---

Ensure queries and ASIM parsers handle nullable/optional fields safely by (1) using type-correct null checks, (2) guarding references to optional/missing columns with `column_ifexists` (and using the same guarded form in both `summarize` and `project`), and (3) gating filters/fields that the source cannot provide so they don’t unintentionally exclude all data; also avoid fabricating empty-string entity fields that mislead consumers.

Practical rules:
1. **Use the right null predicate for the column type**
   - Prefer `isnotnull()` / `isnull()` for typed columns (e.g., `guid`), not `isnotempty()`.
2. **Guard optional columns consistently**
   - If the table/connector may not include a column, reference it as `column_ifexists('col', '<default>')` everywhere it’s used in the query (commonly in both `summarize ... by` and `project`).
3. **Don’t apply filters for fields the source doesn’t have**
   - If the filter parameter exists but the source lacks the corresponding field, gate the filter with an empty-filter condition (e.g., “only filter when the filter array is non-empty”).
4. **Use safe casting + fallbacks**
   - When sources drift in type (string vs guid), normalize with `tostring(...)` + `toguid(...)`, and use `coalesce(...)` to fall through to the next candidate.
5. **Avoid manufacturing empty entity fields**
   - If the source has no entity data, don’t add empty-string entity columns; let them be absent or null according to schema expectations.

Example template:
```kusto
// 1) Optional column guard (use the same guarded expression in summarize + project)
| summarize StartTime=min(TimeGenerated), EndTime=max(TimeGenerated)
  by key1, key2,
     column_ifexists('debugContext_debugData_threatSuspected_s', '')
| project StartTime, EndTime, key1, key2,
          column_ifexists('debugContext_debugData_threatSuspected_s', '')

// 2) Gate filters when the field doesn’t exist in this source
// Only restrict when the filter array is provided; otherwise keep all rows.
| where array_length(srcipaddr) == 0
   or (/* apply srcipaddr filtering here when SrcIpAddr exists */)

// 3) Type-correct null checks
| where isnotnull(abx_body_abx_body_vendorCaseId_g)

// 4) Safe casting for type drift
| extend EventId = coalesce(
    toguid(tostring(column_ifexists('event_id_g',''))),
    toguid(tostring(column_ifexists('event_id_g_guid','')))
  )
```

Adopting these patterns reduces deploy/runtime failures, prevents accidental data drop from missing fields, and ensures null/empty semantics are consistent across environments and sources.