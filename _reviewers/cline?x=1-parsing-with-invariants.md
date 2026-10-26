---
title: Parsing With Invariants
description: 'When implementing algorithms that parse/transform structured inputs
  (external text formats, archives, schemas, metadata), write them as invariant-driven
  parsers: explicitly define record boundaries, handle edge cases deterministically,
  recurse transformations to all relevant depths, and guard against pathological complexity
  or unsafe growth.'
repository: cline/cline?x=1
label: Algorithms
language: TypeScript
comments_count: 8
repository_stars: 70861
---

When implementing algorithms that parse/transform structured inputs (external text formats, archives, schemas, metadata), write them as invariant-driven parsers: explicitly define record boundaries, handle edge cases deterministically, recurse transformations to all relevant depths, and guard against pathological complexity or unsafe growth.

Apply these rules:
- **Boundary-first splitting:** If the format uses delimiters, split with “first N fields” semantics when later fields can contain delimiters (e.g., split on the first two tabs, keep the remainder as the filename).
- **Semantics-preserving path handling:** For records that refer to multiple paths/states (git rename/copy, old vs new paths), preserve the original identity your downstream logic needs; don’t collapse or remap paths without a test.
- **Multi-line span correctness:** For line-oriented formats (YAML frontmatter), compute the span of a top-level entry including its indented continuations; inline scalars must stay one line.
- **Recursive normalization everywhere:** For schema/type transforms, normalize at *all* depths (including `items` and combinators like `anyOf/oneOf/allOf`) before applying object-like gates.
- **Defensive reading with safe defaults:** Treat malformed/older data as absent—drop invalid entries, default missing lists to empty, and avoid lossy caps unless the cap is explicitly part of the correctness model.
- **Complexity & safety guards:** Avoid regex patterns that can backtrack poorly; prefer bounded loops. Enforce limits (max size, max depth/link expansions) while parsing archives or traversing structures.

Checklist (quick):
1) What are the exact record boundaries?
2) Which fields may contain the delimiter?
3) Are identity mappings preserved (old/new paths, roots, names)?
4) Are transformations applied recursively to all schema/AST layers?
5) What happens on malformed input—drop, default, or fail?
6) Any worst-case complexity or unbounded growth paths? If yes, cap or restructure.

Example (boundary-first splitting for tab-containing filenames):
```ts
function parseNumstatRecord(record: string) {
  // Keep remainder as the inline filename (tabs can appear in it).
  const firstTab = record.indexOf("\t");
  const secondTab = record.indexOf("\t", firstTab + 1);
  const add = record.slice(0, firstTab);
  const del = record.slice(firstTab + 1, secondTab);
  const filename = record.slice(secondTab + 1);
  return { add, del, filename };
}
```
