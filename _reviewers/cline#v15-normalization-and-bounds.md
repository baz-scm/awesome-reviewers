---
title: Normalization And Bounds
description: 'When your code derives behavior from external data (schemas, paths,
  formatted text) or computes budgets (tokens, caps), enforce two algorithmic invariants:'
repository: cline/cline#v15
label: Algorithms
language: TypeScript
comments_count: 6
repository_stars: 70877
---

When your code derives behavior from external data (schemas, paths, formatted text) or computes budgets (tokens, caps), enforce two algorithmic invariants:
1) **Normalize/validate the input recursively** before using it. Don’t stop at top-level fields—handle nested/variant structures (arrays, combinators, nested objects). Platform/path and format parsing should produce a canonical representation.
2) **Use domain-accurate bounds/heuristics** instead of naive size arithmetic. Estimates and caps must reflect the real pricing/limits model (e.g., per-image flat costs, per-budget floors/ceilings), and must be protected with explicit upper/lower semantics.

Practical checklist:
- If the input can be nested, write normalization as a recursion over the full type/structure (and add tests that include nested cases).
- Canonicalize paths (e.g., POSIX separators) before comparing/storing.
- For formatted text, implement precedence rules and correctly associate inline values vs block/nested values.
- For token/size computations: never treat base64/payload character counts as proportional cost; use per-item/per-model constants and cap/clamp using correct floor-vs-ceiling logic.
- Add invariant tests for the edge cases that would otherwise “work by accident” today.

Example (recursive normalization pattern):
```ts
function normalizeSchema(schema: any): any {
  const out = { ...schema };
  if (typeof out.type === 'string') out.type = out.type.toLowerCase();

  // Normalize combinators
  for (const key of ['anyOf', 'oneOf', 'allOf']) {
    if (Array.isArray(out[key])) out[key] = out[key].map(normalizeSchema);
  }

  // Normalize items (array/tuple forms)
  if (out.items) {
    if (Array.isArray(out.items)) out.items = out.items.map(normalizeSchema);
    else out.items = normalizeSchema(out.items);
  }

  // Recurse properties for object-like schemas
  if (out.type === 'object' && out.properties && typeof out.properties === 'object') {
    const props: any = {};
    for (const [k, v] of Object.entries(out.properties)) props[k] = normalizeSchema(v);
    out.properties = props;
  }

  return out;
}
```