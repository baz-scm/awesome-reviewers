---
title: Safe identifier renaming
description: 'Treat any exported or widely-referenced identifier (prop names, type
  names, API exports) as semi-public: renaming it can silently break consumers or
  tests. Before merging a rename, grep the whole repo (and check known downstream
  consumers, e.g. DefinitelyTyped) for the old name to ensure no stale references
  remain that could fall through to a default and...'
repository: facebook/react#b18
label: Naming Conventions
language: JavaScript
comments_count: 5
repository_stars: 251889
---

Treat any exported or widely-referenced identifier (prop names, type names, API exports) as semi-public: renaming it can silently break consumers or tests. Before merging a rename, grep the whole repo (and check known downstream consumers, e.g. DefinitelyTyped) for the old name to ensure no stale references remain that could fall through to a default and pass incorrectly (e.g. `expectedEnviromentName` falling back to `|| 'Server'`). When a rename affects a public/semi-public export (e.g. `unstable_Activity` → `Activity`), export both the old and new name during a transition period so downstream code and sync processes aren't broken. When introducing new names, follow the project's established conventions instead of inventing ad hoc ones — e.g. use the `${Verb}${Noun}Options` pattern for options types, and choose names that reflect user-facing semantics rather than internal implementation details (prefer `Promise` over `Thenable` where that's what users actually see). Avoid proliferating multiple naming schemes for the same concept (e.g. `topLevelType` vs `eventName` vs `propName`); consolidate to a single canonical form wherever feasible. Document and apply these conventions consistently so future renames and additions don't require re-litigating naming decisions.