---
title: Guard parser edge cases
description: 'When writing custom parsers or recursive traversal logic over structured
  or external data (git output, file trees, tarballs, YAML), explicitly enumerate
  and handle boundary conditions rather than assuming a simplified shape. Common failure
  modes to check for:'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Algorithms
language: TypeScript
comments_count: 6
repository_stars: 70965
---

When writing custom parsers or recursive traversal logic over structured or external data (git output, file trees, tarballs, YAML), explicitly enumerate and handle boundary conditions rather than assuming a simplified shape. Common failure modes to check for:

- Delimiters that can legitimately appear inside the data itself (e.g. a filename containing a tab breaking a naive `split("\t")`; only the first N expected separators should be treated as structural, with the remainder joined back as the real content).
- Special-cased entries that don't follow the general format (e.g. git submodules/gitlinks have no blob content and must be rendered the way git itself shows them, not treated as a regular file diff).
- Degenerate/root inputs (e.g. normalizing a path must not collapse a legitimate filesystem root like `/` or `C:\`).
- Multi-line or block-scalar entries whose span must be computed correctly so trailing comments or continuation lines aren't misattributed.
- Recursive or graph-like structures (symlinks, directory trees) that can cycle back on themselves or expand exponentially; add explicit cycle detection and a hard cap on recursion depth/expansion count so malicious or accidental loops terminate quickly instead of hanging or blowing up memory.

For every such algorithm, write a test that exercises the adversarial case (tab in a filename, a symlink loop, a filesystem root, a submodule, a one-line vs. multi-line YAML value) in addition to the happy path. When fixing a parsing or traversal bug, prefer deriving the fix from the actual format/structure semantics (e.g. matching `git diff`'s own rendering) rather than patching around the specific failing input.

Example (tab-safe numstat parsing):
```ts
// Only the first two tabs are separators; filenames may contain tabs.
const [add, del, ...pathParts] = record.split("\t");
const path = pathParts.length ? pathParts.join("\t") : undefined;
```

Example (bounded, cycle-safe symlink expansion):
```ts
function addLinked(relativePath: string, repoPath: string, target: string, depth: number) {
  if (depth > MAX_LINK_DEPTH || isAncestorOrSelf(resolved, copyChain)) {
    skippedPaths.push(repoPath);
    return;
  }
  // ...expand, tracking expansions against MAX_LINK_EXPANSIONS
}
```