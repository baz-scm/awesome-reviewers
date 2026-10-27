---
title: Simplify redundant code
description: 'Favor the most direct, concise expression of logic and eliminate unnecessary
  indirection, parameters, or branching. Before submitting code, look for opportunities
  to:'
repository: facebook/react#b18
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 251889
---

Favor the most direct, concise expression of logic and eliminate unnecessary indirection, parameters, or branching. Before submitting code, look for opportunities to:
- Replace verbose if/else blocks with a ternary or simple boolean expression when the logic is a single conditional value, e.g. prefer `declarator.init != null ? declarator.init : t.identifier('undefined')` over a multi-line if/else returning the same assignment expression.
- Remove helper functions or extra computed values when an existing comparison already expresses the intent (e.g. comparing `prop.originalName !== prop.newName` instead of introducing a separate `isHyphenatedJsxProp()` helper).
- Avoid passing data through function parameters when it's already reachable from an object already in scope (e.g. don't pass `env` separately if it's accessible via `hir.env`).
- Merge related conditional branches that check mutually exclusive flags into a single if/else-if chain rather than separate, overlapping `if` statements.
- Prefer functions that return values explicitly over functions that mutate an output parameter as a side effect; if mutation is unavoidable, name the parameter and function clearly to make the side effect obvious (e.g. `collectFnGlobalDeps(fn, deps)` instead of an ambiguous `getFnGlobalDeps`).

These small simplifications reduce cognitive load, make intent clearer, and minimize the surface area for bugs introduced by redundant state or logic.