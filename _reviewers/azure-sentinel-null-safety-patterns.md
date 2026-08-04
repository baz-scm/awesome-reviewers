---
title: Null Safety Patterns
description: When fields or parameters are optional (may be missing, null, or empty-string),
  code must be defensive so queries/playbooks/parsers don’t fail and so “unknown”
  stays unknown.
repository: Azure/Azure-Sentinel
label: Null Handling
language: Json
comments_count: 7
repository_stars: 6042
---

When fields or parameters are optional (may be missing, null, or empty-string), code must be defensive so queries/playbooks/parsers don’t fail and so “unknown” stays unknown.

Do this:
- Use `isempty()` / `isnotempty()` instead of `isnull()` when source can be `""` (empty string) as well as null.
  - Example: `TimeGenerated=iff(isempty(EventDate), now(), todatetime(EventDate))`
- Before casting/using optional values, guard with `isnotempty` so empty-string doesn’t coerce to a valid value (e.g., `0`).
  - Example: `SourcePort = iff(isnotempty(SourcePort), toint(SourcePort), int(null))`
- For optional arrays/fields used in string building or JSON/table output, wrap with `coalesce` (and a safe empty value).
  - Example: `labelsSafe = coalesce(Indicator.labels, createArray())`
- For KQL that might run against missing columns, prefer `column_ifexists(<col>, <default>)` (or ensure the parser guarantees the schema used by the workbook).
- For Sentinel parser/function definitions, never remove/omit default `functionParameters` values unless the query logic can handle parameters being unspecified.

If you apply these patterns consistently, you prevent runtime failures from missing fields/columns and avoid silent data-quality issues caused by incorrect null/empty handling.