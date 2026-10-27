---
title: Prefer simple, self-documenting code
description: 'Favor straightforward, idiomatic code over clever or unnecessarily abstracted
  constructs. Specifically:


  - Avoid magic numbers/values with explanatory comments; derive them from the source
  so they stay correct and self-documenting. E.g., prefer `name.slice(''<anonymous>.''.length)`
  over `name.slice(12) // 12 is the length of ''<anonymous>.''`, since the former...'
repository: facebook/react#b20
label: Code Style
language: JavaScript
comments_count: 6
repository_stars: 251895
---

Favor straightforward, idiomatic code over clever or unnecessarily abstracted constructs. Specifically:

- Avoid magic numbers/values with explanatory comments; derive them from the source so they stay correct and self-documenting. E.g., prefer `name.slice('<anonymous>.'.length)` over `name.slice(12) // 12 is the length of '<anonymous>.'`, since the former is inlined at build time and needs no comment.
- Use strict equality (`===`/`!==`) by default; only use weak equality when there's a specific, documented reason.
- Simplify conditional/ternary expressions and string interpolation instead of duplicating near-identical branches, e.g. `` `${isProfiling ? 'Stop' : 'Start'} profiling - ${shortcut}` `` instead of two separate `title` variables built from an if/else.
- Remove redundant attributes, comments, or UI text that repeat information already conveyed elsewhere (e.g., a `title="Report bug"` on a link whose visible text already says "Report bug").
- Avoid introducing new abstraction helpers (e.g., `isSomething(...)` checks) when the existing control flow (switch statements, if/else branches) already expresses the same logic clearly. Prefer forking behavior directly within existing control flow over adding indirection layers, even if it means a bit more explicit/duplicated code, since that keeps the flow easy to follow and avoid a proliferation of single-purpose predicate functions.

When reviewing code, prefer the version that reads clearly on its own, minimizes indirection/magic values, and avoids duplication of information or logic that the language/runtime already makes obvious.</description>
</invoke>
