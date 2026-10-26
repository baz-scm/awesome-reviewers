---
title: Bounded Normalization Algorithms
description: 'For any algorithm that transforms structured data (schemas, estimators,
  parsers, path/string normalization), require:


  - **Deterministic normalization:** Normalize inputs to a canonical form (e.g., consistent
  separators, case, and precedence rules) rather than relying on incidental runtime/platform
  formatting.'
repository: cline/cline#v22
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 70886
---

For any algorithm that transforms structured data (schemas, estimators, parsers, path/string normalization), require:

- **Deterministic normalization:** Normalize inputs to a canonical form (e.g., consistent separators, case, and precedence rules) rather than relying on incidental runtime/platform formatting.
- **Full recursion/coverage:** If the input is nested (arrays/items, combinators, object properties), ensure normalization/validation is applied at every depth and branch.
- **Bounded work:** Avoid operations with potential pathological performance (e.g., regex patterns that can backtrack badly) and enforce practical caps (sizes/time/buffer limits) for untrusted data.
- **Edge-focused tests:** Add tests for the tricky cases the heuristic/normalizer might mishandle (large encoded payloads, nested structures, platform-specific path characters).

Example patterns to follow:

```ts
// 1) Avoid char-count heuristics for base64 images; keep estimation bounded and per-image.
// (Test that estimate does not explode with payload length.)

// 2) Ensure schema normalization recurses into nested branches.
function normalizeType(schema: any): any {
  const s = { ...schema };
  if (typeof s.type === "string") s.type = s.type.toLowerCase();
  // Recurse into nested forms before/after any object-like gate.
  if (s.items) s.items = normalizeType(s.items);
  if (s.anyOf) s.anyOf = s.anyOf.map(normalizeType);
  if (s.oneOf) s.oneOf = s.oneOf.map(normalizeType);
  if (s.allOf) s.allOf = s.allOf.map(normalizeType);
  if (s.properties) {
    for (const [k, v] of Object.entries(s.properties)) s.properties[k] = normalizeType(v);
  }
  return s;
}

// 3) Keep path normalization deterministic across platforms.
// Convert using POSIX separators in a controlled way (don’t accidentally treat a literal backslash as a separator).
const rel = toPosixSeparators(path.relative(workspaceRoot, line));

// 4) Prefer loops over regexes with known worst-case backtracking risks,
// and enforce size limits when reading/parsing untrusted archives.
```

Adopt this as a checklist: (a) Can the algorithm be tricked by nested/encoded inputs? (b) Is the transformation canonical and deterministic? (c) Is work bounded and non-pathological? (d) Do tests cover at least one adversarial edge case per rule above? 