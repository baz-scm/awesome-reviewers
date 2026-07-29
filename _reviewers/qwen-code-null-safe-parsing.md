---
title: Null-Safe Parsing
description: 'Enforce null/optional safety at every boundary: treat external API data
  and persisted JSON as untrusted, validate before dereferencing, and ensure normalization/parsing
  preserves only values that satisfy the declared type contract. Never let invalid
  optional fields “leak through” via `...raw` spreads or falsy-based numeric checks;
  degraded modes must remain...'
repository: QwenLM/qwen-code
label: Null Handling
language: TypeScript
comments_count: 9
repository_stars: 26407
---

Enforce null/optional safety at every boundary: treat external API data and persisted JSON as untrusted, validate before dereferencing, and ensure normalization/parsing preserves only values that satisfy the declared type contract. Never let invalid optional fields “leak through” via `...raw` spreads or falsy-based numeric checks; degraded modes must remain structurally consistent so downstream consumers don’t misinterpret missing facts.

Practical rules:
- Guard optional/conditionally-present fields before dereferencing (fail per-item, not per-loop).
- In `normalize*` functions, construct the output from known fields (or delete known invalid fields after `...raw`). Avoid `...raw` followed by conditional spreads that can’t overwrite wrong-typed values.
- Never use truthiness to validate numbers where `0` is valid; check `typeof x === 'number' && Number.isFinite(x)`.
- If a function’s contract says “never throws”, explicitly handle valid JSON `null`/non-object inputs.
- When prerequisites are missing (e.g., worktree absent), emit consistent flags and neutral placeholders (`unknown`/`null`) rather than silently degrading to “unchanged”.

Example (safe normalization + “never throws”):
```ts
type Out = { hostAuthToken?: string };

function stringOrUndefined(v: unknown): string | undefined {
  return typeof v === 'string' ? v : undefined;
}

export function normalizeWorker(raw: unknown): Out {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return {};
  const r = raw as Record<string, unknown>;
  // Do NOT `return { ...raw, ... }` (it can leak wrong-typed optional fields).
  return {
    hostAuthToken: stringOrUndefined(r.hostAuthToken),
  };
}

export function parseReceiptIds(raw: string): number[] {
  try {
    const parsed = JSON.parse(raw);
    if (parsed === null || typeof parsed !== 'object') return [];
    const o = parsed as Record<string, unknown>;
    const ids = Array.isArray(o.reviewIds)
      ? o.reviewIds
      : typeof o.reviewId === 'number'
        ? [o.reviewId]
        : [];
    return ids.filter((x): x is number => typeof x === 'number' && Number.isInteger(x));
  } catch {
    return [];
  }
}
```

Applying this will prevent both crash-on-null (wedge/stall) and silent misclassification (wrong “clean” or “unknown” signals).