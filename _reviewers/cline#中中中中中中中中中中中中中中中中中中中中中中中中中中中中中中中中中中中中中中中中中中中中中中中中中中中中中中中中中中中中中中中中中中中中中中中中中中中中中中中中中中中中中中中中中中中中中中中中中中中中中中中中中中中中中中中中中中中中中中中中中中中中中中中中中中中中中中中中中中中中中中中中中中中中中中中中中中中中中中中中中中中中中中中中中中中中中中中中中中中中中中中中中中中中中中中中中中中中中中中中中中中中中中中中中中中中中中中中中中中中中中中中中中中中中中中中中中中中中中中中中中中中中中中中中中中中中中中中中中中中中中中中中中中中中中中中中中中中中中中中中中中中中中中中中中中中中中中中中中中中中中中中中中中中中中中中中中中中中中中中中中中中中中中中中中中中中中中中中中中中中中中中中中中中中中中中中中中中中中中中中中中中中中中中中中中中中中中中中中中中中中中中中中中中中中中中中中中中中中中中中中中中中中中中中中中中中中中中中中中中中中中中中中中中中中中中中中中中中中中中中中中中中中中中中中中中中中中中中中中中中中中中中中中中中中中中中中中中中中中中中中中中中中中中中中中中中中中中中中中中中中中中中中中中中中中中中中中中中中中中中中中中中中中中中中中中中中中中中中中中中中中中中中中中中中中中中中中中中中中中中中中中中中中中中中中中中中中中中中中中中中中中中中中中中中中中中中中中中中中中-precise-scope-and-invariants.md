---
title: Precise scope and invariants
description: When an algorithm processes a bounded slice of data — a window of messages,
  the line span of a parsed entry, a set of selectable items, a tree merge, a diff
  side — explicitly define and verify the boundary conditions and invariants it depends
  on, rather than approximating them.
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Algorithms
language: TypeScript
comments_count: 7
repository_stars: 70984
---

When an algorithm processes a bounded slice of data — a window of messages, the line span of a parsed entry, a set of selectable items, a tree merge, a diff side — explicitly define and verify the boundary conditions and invariants it depends on, rather than approximating them.

Concretely:
- State the exact scope rule and why it holds. For example, scanning messages for "facts about the last turn" must stop at the newest real user prompt, not accumulate across turns; a parsed entry's line span must distinguish single-line scalars from block scalars with continuation lines.
- Identify items by a stable key (an id, a stage, a mode), not by transient position (index, iteration order), when the underlying collection can be filtered, reordered, or reused across calls (e.g. skip/unskip acting on `itemId` rather than a cursor position).
- When an algorithm assumes a data-structure invariant (e.g. two trees being merged have disjoint path sets, a submodule's working directory being its own repo root, a merge conflict's index having a stage-0 vs stage-2/3 entry), verify that invariant explicitly or guard against its violation — don't rely on an assumption nobody checked.
- When replicating behavior of a reference system (git's symlink storage, submodule dirty-state, conflict resolution, diff semantics), mirror its actual algorithm rather than inventing a plausible-looking approximation, and add a test against the real tool to confirm the match.

Example pattern for scoping to "this turn only":
```ts
// Wrong: scans all messages, letting a prior turn's edits/errors leak in.
for (const message of messages) { ... }

// Right: bound the scan to messages after the newest real prompt.
const turnStart = messages.findLastIndex(m => m.role === "user" && m.userRunSpan !== 0);
for (const message of messages.slice(turnStart)) { ... }
```

Getting these boundaries and invariants wrong produces subtly incorrect results (stale state bleeding across turns, wrong item being skipped, diffs that don't match what the tool actually shows) that are easy to miss in review and only surface in edge cases — so call out the boundary/invariant explicitly in code and cover it with a test that exercises the edge case.