---
title: Bounded, cycle-safe traversal
description: When an algorithm recurses or iterates over a structure that can contain
  cycles or unbounded chains (symlinks, graph edges, paginated state transitions),
  it must both detect cycles and cap the amount of work it will do, rather than relying
  on the input being well-formed. For example, when resolving a symlink target that
  may point back into a directory...
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 71067
---

When an algorithm recurses or iterates over a structure that can contain cycles or unbounded chains (symlinks, graph edges, paginated state transitions), it must both detect cycles and cap the amount of work it will do, rather than relying on the input being well-formed. For example, when resolving a symlink target that may point back into a directory already being copied (`.`, `..`, or a sibling link forming a loop), track the chain of directories currently being expanded and skip any target that revisits one of them, in addition to imposing a hard cap on the number of expansions — so a handful of adversarial or accidental cycles cannot hang the operation or blow the stack.

The same discipline applies to algorithms that maintain state across a sequence of operations (e.g. a cursor into a paged list, or ids that must stay stable as the underlying collection changes): define the invariant precisely (e.g. "skipping a row removes only that row and leaves the others in place," "a cycle is skipped and recorded, not re-expanded") and write it down as an explicit rule, then verify it holds not just for the one sequence in the bug report but for many sequences. Property-based or fuzz tests that replay thousands of random operation sequences against the stated invariant are an effective way to catch the class of bug, not just the one instance:

```ts
// Example invariant for a cycle-prone expansion algorithm:
// "a link whose target is an ancestor of, or equal to, a directory
// already being expanded is skipped and recorded, not re-expanded"
// and a hard cap on total expansions as a backstop.
if (isAncestorOrSelf(resolvedTarget, expansionChain) || expansions > MAX_LINK_EXPANSIONS) {
  skippedPaths.push(repoPath);
  return;
}
```

Before merging any recursive/iterative algorithm over externally influenced or mutable structures, ask: what stops this from looping forever, and what test proves it for more than the one example in the PR?