---
title: Type-safe query contracts
description: 'When a UI route consumes or produces URL search/query parameters, treat
  those parameters as a contract: validate and type them at the route boundary, update
  them through typed helpers (no `as any`), and normalize/omit default-derived fields
  so the resulting query set is consistent.'
repository: looplj/axonhub
label: API
language: TSX
comments_count: 2
repository_stars: 4808
---

When a UI route consumes or produces URL search/query parameters, treat those parameters as a contract: validate and type them at the route boundary, update them through typed helpers (no `as any`), and normalize/omit default-derived fields so the resulting query set is consistent.

Apply:
- Add a search validator/type for list/detail routes (or the routing layer) so `navigate({ search })` matches the route’s expected schema.
- Prefer a single typed helper that updates a `draft: Record<string, unknown>` (or a stronger type) and returns the next search object.
- Normalize composite params (e.g., date ranges): only write “time” keys when their corresponding date keys are present; omit default time values to avoid noisy or inconsistent URLs.

Example (TypeScript):
```ts
// Route boundary: validate search
// (Exact API depends on your router, but the idea is: no implicit/unchecked shape)
// validateSearch: (s) => Record<string, unknown>

function updateRequestSearch(
  apply: (draft: Record<string, unknown>) => void,
) {
  const nextSearch = (prev: Record<string, unknown> | undefined) => {
    const draft: Record<string, unknown> = { ...(prev ?? {}) };
    apply(draft);
    return draft;
  };

  navigate({
    search: nextSearch as any, // only if your router typing requires; ideally remove this via proper validateSearch types
    replace: true,
  });
}

function onDateRangeChange(range?: DateTimeRangeValue) {
  updateRequestSearch((draft) => {
    const normalized = range ? normalizeDateTimeRangeValue(range) : undefined;

    if (!normalized || (!normalized.from && !normalized.to)) {
      delete draft.createdAtFrom;
      delete draft.createdAtTo;
      delete draft.createdAtStartTime;
      delete draft.createdAtEndTime;
      return;
    }

    if (normalized.from) draft.createdAtFrom = formatSearchDate(normalized.from);
    else delete draft.createdAtFrom;

    if (normalized.to) draft.createdAtTo = formatSearchDate(normalized.to);
    else delete draft.createdAtTo;

    // Only keep time fields when the corresponding date side exists,
    // and omit defaults (e.g., 00:00:00 / 23:59:59) in your formatter.
    draft.createdAtStartTime = formatSearchTime(normalized.startTime);
    draft.createdAtEndTime = formatSearchTime(normalized.endTime);
  });
}
```
