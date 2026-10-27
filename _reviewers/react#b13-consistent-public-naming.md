---
title: Consistent Public Naming
description: 'When changing or introducing names (props, exported types, public exports,
  user-visible labels, flags), treat them as cross-module/public API: follow the established
  naming conventions, normalize naming at the boundary, and preserve compatibility
  explicitly.'
repository: facebook/react#b13
label: Naming Conventions
language: JavaScript
comments_count: 7
repository_stars: 251893
---

When changing or introducing names (props, exported types, public exports, user-visible labels, flags), treat them as cross-module/public API: follow the established naming conventions, normalize naming at the boundary, and preserve compatibility explicitly.

Apply this checklist:
1) **No silent fallback for renamed identifiers**: if a prop/field name changed, ensure all call sites/fixtures are updated—avoid situations where old misspellings still hit a default and tests pass.
2) **Normalize at the source**: if you’re repeatedly converting between naming schemes across layers (e.g., `topPress` ⇄ `press` / `onPress`), move the normalization to the boundary so downstream logic doesn’t duplicate prefix-stripping checks.
3) **Use the established convention for the kind of name**: e.g., `*Options` for option bags, consistent suffixes for static vs render-specific concepts, and consistent user-facing labels in tooling.
4) **Explicit compatibility aliases for public exports**: when renaming a public API, export both names (e.g., new primary name plus old name as an alias) rather than breaking consumers.

Example patterns:
- Avoid misspelled identifiers relying on defaults:
```js
// Don’t let an old misspelling silently fall back.
// Ensure all uses are updated repo-wide.
this.props.expectedEnvironmentName || 'Server';
```
- Normalize event naming once (instead of many scattered checks):
```js
// Prefer normalizing dispatch naming so downstream doesn’t keep re-parsing prefixes.
export function topLevelTypeToEventName(topLevelType) {
  return topLevelType.startsWith('top') ? topLevelType.slice(3).toLowerCase() : topLevelType;
}
```
- Preserve compatibility with explicit aliases:
```js
export {Activity, Activity as unstable_Activity};
```