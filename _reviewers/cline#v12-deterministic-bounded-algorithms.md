---
title: Deterministic Bounded Algorithms
description: 'When implementing algorithmic transformations (IDs, token estimates,
  schema normalization, cap/floor logic), treat invariants and complexity as first-class
  requirements:'
repository: cline/cline#v12
label: Algorithms
language: TypeScript
comments_count: 6
repository_stars: 70872
---

When implementing algorithmic transformations (IDs, token estimates, schema normalization, cap/floor logic), treat invariants and complexity as first-class requirements:

- **Define invariants explicitly** (e.g., stable IDs must not change when only irrelevant text changes beyond published bounds; token estimates must be invariant to image base64 length; output caps must follow intended floor/ceiling rules).
- **Normalize/clip early** so downstream steps (hashing/estimation) operate on the same canonical representation.
- **Make transformations structurally complete**: when normalizing nested structures, recurse into all structural paths (e.g., `items`, `anyOf`/`oneOf`/`allOf`) *before* applying object-like gates/filters.
- **Enforce bounds**: cap work and avoid heuristics that scale with the wrong dimension (e.g., char-counting base64 payloads for token estimates). Use tests that target the failing dimension.
- **Lock behavior with edge-case tests** (long payloads, nested schemas, different model budgets, skipped/overlapping paths semantics).

Example (hashing with invariants):
```ts
const PROMPT_MAX = 400; 
const WHY_MAX = 200;
const fnv1a32 = (s: string) => /* stable hash */ '';

function suggestionId(kind: string, prompt: string, why: string) {
  const p = prompt.slice(0, PROMPT_MAX);
  const w = why.slice(0, WHY_MAX);
  // Canonical inputs => deterministic IDs
  return fnv1a32(`${kind}:${p}:${w}`);
}
```

Checklist for new/changed algorithmic logic:
1) What must stay invariant? 2) What is the canonical input representation? 3) Is recursion complete for all structural variants? 4) What bounds prevent scaling on the wrong dimension? 5) Do tests cover the edge cases that would otherwise break invariants or bounds?