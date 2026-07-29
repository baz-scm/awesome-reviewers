---
title: Normalize selection keys
description: 'When selecting a “preferred” item (via `find`, `filter`, pagination
  anchors, etc.) or deciding based on a computed threshold, ensure two things:

  1) **Compare like with like:** normalize/parse inputs so the keys you compare are
  in the same canonical form.'
repository: QwenLM/qwen-code
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 26407
---

When selecting a “preferred” item (via `find`, `filter`, pagination anchors, etc.) or deciding based on a computed threshold, ensure two things:
1) **Compare like with like:** normalize/parse inputs so the keys you compare are in the same canonical form.
2) **Use explicit priority + fallback:** run a primary search first; only if it yields nothing should you consult a fallback source. Avoid making fallback evidence primary.

Practical checklist:
- If settings/identifiers may be encoded (e.g., `authType:modelId`), always decode/resolve to the same shape before comparing to stored objects.
- If multiple event sources can provide the anchor/marker, implement a 2-pass selection: (a) search preferred sources, (b) if none found, use fallback.
- For threshold/budget calculations that depend on layout, include **all** relevant contributing elements (missing siblings/gaps can flip thresholds).

Code pattern (key normalization + prioritized fallback):
```ts
// 1) Normalize first (so comparisons match)
const normalized = isCompactionMode
  ? resolveModelId(settings?.merged?.compactionModel?.trim() ?? '')
  : undefined;

// 2) Primary then fallback
const preferred = (() => {
  // primary: use the most reliable/expected source(s)
  const primary = normalized
    ? availableModelEntries.find(({ authType, model }) =>
        authType &&
        authType === normalized.authType &&
        model.id === normalized.modelId
      )
    : undefined;

  if (primary) return primary;

  // fallback: weaker/secondary match only if primary failed
  return availableModelEntries.find(({ model }) => model.id === normalized?.modelId);
})();
```
Apply this same approach to anchor selection and transcript pagination: prefer `session_update`-derived ids first; only if absent should you use the `history_truncated` marker id.