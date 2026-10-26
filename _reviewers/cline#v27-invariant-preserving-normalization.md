---
title: Invariant-preserving Normalization
description: 'When writing parsing/normalization/transform algorithms, make correctness
  a property of explicit invariants: handle the full input space (nested branches,
  combinators, delimiter edge cases), ensure termination for worst cases (avoid pathological
  operations and cap/skip expansions), and lock invariants with targeted + property/fuzz-style
  tests.'
repository: cline/cline#v27
label: Algorithms
language: TypeScript
comments_count: 6
repository_stars: 70892
---

When writing parsing/normalization/transform algorithms, make correctness a property of explicit invariants: handle the full input space (nested branches, combinators, delimiter edge cases), ensure termination for worst cases (avoid pathological operations and cap/skip expansions), and lock invariants with targeted + property/fuzz-style tests.

Practical checklist
- **Specify the invariant**: e.g., “skip hides only the target row”, “rename unstages must use original path”, “split numstat only on first two tabs”, “schema type normalization applies at every depth”, “plural categories must match CLDR exactly”.
- **Make splitting/decoding rules precise**: limit splits (e.g., only first N delimiters) so filenames/fields containing delimiters are preserved.
- **Normalize/transform recursively and completely**: recurse through all container shapes and combinators (arrays/tuples, anyOf/oneOf/allOf, nested objects), not just top-level fields.
- **Guarantee safe termination/performance**: avoid regex patterns that can blow up on long inputs; prefer linear scans; add caps for graph/link expansion loops and treat cycles as “skip”.
- **Test the invariants, not just examples**:
  - Add **edge-case unit tests** for delimiter/path/nesting cases.
  - Add **property/fuzz tests** when the behavior is stateful or when invariants should hold across many operation sequences.

Mini example (recursive, invariant-based normalization with termination guard)
```ts
type Node =
  | { type: string; properties?: Record<string, unknown>; items?: unknown }
  | { anyOf?: unknown[] } | { oneOf?: unknown[] } | { allOf?: unknown[] };

function normalizeTypes(node: unknown, depth = 0): unknown {
  if (depth > 50) return node; // termination guard for adversarial nesting
  if (!node || typeof node !== 'object') return node;

  const n = node as any;
  const type = typeof n.type === 'string' ? n.type.toLowerCase() : n.type;

  // Recurse into combinator branches
  if (Array.isArray(n.anyOf)) return { ...n, anyOf: n.anyOf.map(x => normalizeTypes(x, depth + 1)) };
  if (Array.isArray(n.oneOf)) return { ...n, oneOf: n.oneOf.map(x => normalizeTypes(x, depth + 1)) };
  if (Array.isArray(n.allOf)) return { ...n, allOf: n.allOf.map(x => normalizeTypes(x, depth + 1)) };

  // Recurse into object/array shapes
  if (type && (type === 'object' || n.properties || n.required || n.additionalProperties)) {
    const props = n.properties && typeof n.properties === 'object'
      ? Object.fromEntries(Object.entries(n.properties).map(([k, v]) => [k, normalizeTypes(v, depth + 1)]))
      : n.properties;
    return { ...n, type, properties: props };
  }

  if (n.items) return { ...n, type, items: normalizeTypes(n.items, depth + 1) };
  return { ...n, type };
}
```

Use this standard to review algorithms that parse external formats, normalize structured data, paginate state machines, or expand graph-like structures: if the code can’t clearly explain its invariant and its termination/recursion coverage—and if tests don’t defend the invariant under edge cases—treat it as incomplete.