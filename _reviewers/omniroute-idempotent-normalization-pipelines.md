---
title: Idempotent normalization pipelines
description: When code must normalize or classify structured data (messages, request
  bodies, model/provider selection, metrics), implement it as deterministic, *idempotent*,
  and *non-mutating* transformations.
repository: diegosouzapw/OmniRoute
label: Algorithms
language: TypeScript
comments_count: 7
repository_stars: 33162
---

When code must normalize or classify structured data (messages, request bodies, model/provider selection, metrics), implement it as deterministic, *idempotent*, and *non-mutating* transformations.

Apply these rules:
- **Normalize shapes with explicit merge/update rules**: if an external API rejects a structure (e.g., consecutive same-role entries), implement a function that enforces the required invariant (e.g., merge adjacent same-role items).
- **Keep transformations idempotent**: prepends/appends should be guarded by an idempotency key or prefix/text detection so re-running the pipeline doesn’t duplicate content.
- **Avoid unintended mutation**: if you transform an array/object derived from caller input, copy the elements/arrays you modify.
- **Use precise matching for classification**: prefer boundary-aware regex or generalized capability checks over naive `includes()` where false positives are possible.
- **Ensure aggregation update rules are correct**: when computing totals, accumulate instead of overwriting per-group values.

Example (non-mutating consecutive-role merge + idempotent ops sketch):
```ts
type Content = { role: string; parts: Array<{ text: string }> };

function mergeConsecutiveSameRole(contents: Content[]): Content[] {
  const merged: Content[] = [];
  for (const entry of contents) {
    const last = merged[merged.length - 1];
    if (last && last.role === entry.role) {
      // mutate only the new output copy
      last.parts.push(...entry.parts);
    } else {
      // prevent caller mutation
      merged.push({ ...entry, parts: [...entry.parts] });
    }
  }
  return merged;
}

type Op = { kind: 'prepend_system_block'; text: string; idempotencyKey?: string };
function applyOp(blocks: Array<{ type: 'text'; text: string }>, op: Op) {
  const alreadyThere = blocks.some((b) => b.text === op.text || b.text.startsWith(op.text));
  return alreadyThere ? blocks : [{ type: 'text', text: op.text }, ...blocks];
}
```

Practical checklist:
- Add regression tests for (a) repeated execution, (b) edge input shapes (empty/missing fields), and (c) realistic provider/model strings to prevent matching errors.
- For metrics/analytics, add tests that verify accumulation (`sum += value`) rather than overwriting. If you follow these, you’ll prevent the common failure modes seen across the discussions: invalid request shapes, duplicated system blocks, false-positive classification, and incorrect aggregation totals.