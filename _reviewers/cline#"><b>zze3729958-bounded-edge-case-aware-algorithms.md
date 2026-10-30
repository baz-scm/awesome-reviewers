---
title: Bounded, edge-case-aware algorithms
description: 'When writing algorithms that parse text, split on delimiters, or traverse
  recursive/graph-like structures (symlinks, trees, nested frontmatter), explicitly
  enumerate and test the boundary conditions rather than relying on a "common case"
  implementation:'
repository: cline/cline#"><b>zze3729958
label: Algorithms
language: TypeScript
comments_count: 8
repository_stars: 71067
---

When writing algorithms that parse text, split on delimiters, or traverse recursive/graph-like structures (symlinks, trees, nested frontmatter), explicitly enumerate and test the boundary conditions rather than relying on a "common case" implementation:

- **Delimiter/encoding boundaries**: splitting on a character (tabs, newlines) must account for that character legitimately appearing inside the data (e.g. filenames containing tabs should split only on the first N separators, not all of them); string slicing must be aware of multi-unit encodings (UTF-16 surrogate pairs) so truncation never cuts a code unit in half; trimming logic must preserve semantically significant characters (a root path's trailing separator is not the same as a nested path's).
- **Degenerate/short inputs**: guard heuristics (e.g. partial-line or fuzzy matching) against trivial inputs where the heuristic produces false positives (very short strings matching almost everything).
- **Cyclic or self-referential traversal**: any recursive or iterative traversal over structures that can contain cycles or self-references (symlinks pointing at ancestors/siblings, directory links that re-expand each other) must track visited state or cap recursion depth/iteration count, and must cap the total amount of work done (e.g. `MAX_LINK_DEPTH`, `MAX_LINK_EXPANSIONS`) so a crafted or accidental cycle fails fast instead of hanging or exhausting memory.
- **Clear decomposition**: when a parsing routine has several distinct cases (grammar alternatives), prefer expressing it as a sequence of explicit "take while X" / "take one Y if present" steps that consume from the front of the input, over an ad hoc loop that mutates shared state and inspects previously-produced output. This keeps each case testable in isolation and avoids side effects bleeding across iterations.

Example of bounding a potentially cyclic expansion:

```ts
const MAX_LINK_DEPTH = 8;
const MAX_LINK_EXPANSIONS = 200;
let expansions = 0;

function resolveLink(path: string, depth: number): Entry | undefined {
  if (depth > MAX_LINK_DEPTH || ++expansions > MAX_LINK_EXPANSIONS) {
    skippedPaths.push(path);
    return undefined;
  }
  // ...follow the link, recursing with depth + 1
}
```

Every such edge case should have a regression test that exercises it directly (e.g. a tab-containing filename, a surrogate pair at a truncation boundary, a symlink cycle), not just the happy path.