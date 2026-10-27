---
title: Naming as API
description: 'Treat public (or effectively public) identifier names—props, exported
  symbols, Flow types, and semantic labels—as API surface.


  Apply these rules:

  1) Follow existing naming conventions/patterns'
repository: facebook/react#b4
label: Naming Conventions
language: JavaScript
comments_count: 6
repository_stars: 251885
---

Treat public (or effectively public) identifier names—props, exported symbols, Flow types, and semantic labels—as API surface.

Apply these rules:
1) Follow existing naming conventions/patterns
- Prefer the project’s established conventions (e.g., `*Options` for options types; reuse existing semantic naming logic like using the “Promise” name when the value behaves like a promise).

2) Make renames safe and non-silent
- Avoid misspellings and fallbacks that let incorrect identifiers pass tests.
- After renaming, run a repo-wide search for the old spelling and update all call sites/fixtures.

3) Canonicalize naming at the boundary
- Don’t duplicate conversion/mapping logic across the codebase.
- If two naming conventions exist (e.g., RN native `topPress` vs React `press`/`onPress`), choose a canonical representation early (e.g., strip `top` at dispatch) and simplify downstream logic.

4) Preserve compatibility with explicit aliases
- When stabilizing an “unstable_” export, export the new name and keep a compatibility alias.

Example patterns:
```js
// 1) Don’t let a renamed prop silently fall back due to a typo
// BAD (typo keeps working):
const name = props.expectedEnviromentName || 'Server';
// GOOD:
const name = props.expectedEnvironmentName || 'Server';

// 2) Preserve compatibility when renaming exports
export { Activity };
export { Activity as unstable_Activity };

// 3) Canonicalize early to avoid repeated mapping logic
// Instead of mapping multiple times downstream, normalize at the boundary:
function nativeToCanonicalEventName(topLevelType) {
  return topLevelType.startsWith('top') ? topLevelType.slice(3).toLowerCase() : topLevelType;
}
```

Checklist to apply in PRs:
- Are we changing/adding any identifier that is exported, referenced by external consumers, or used by tests/fixtures? If yes, verify convention alignment and compatibility.
- After a rename, did we search for the old identifier spelling and update all usages?
- Did we introduce duplicate naming-translation logic that should be canonicalized once?