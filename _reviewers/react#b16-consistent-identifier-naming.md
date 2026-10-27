---
title: Consistent Identifier Naming
description: 'Use one clear naming scheme end-to-end, and treat public/semi-public
  names as compatibility contracts.


  **Do**

  - **Verify global renames**: when changing an identifier (prop, option key, dataset
  key, etc.), confirm there are no remaining misspellings/old spellings that can silently
  take defaults.'
repository: facebook/react#b16
label: Naming Conventions
language: JavaScript
comments_count: 5
repository_stars: 251891
---

Use one clear naming scheme end-to-end, and treat public/semi-public names as compatibility contracts.

**Do**
- **Verify global renames**: when changing an identifier (prop, option key, dataset key, etc.), confirm there are no remaining misspellings/old spellings that can silently take defaults.
- **Normalize naming at the source**: avoid repeating “name translation” logic across layers. If a prefix/convention is the root cause (e.g., RN `top*` event types), remove/normalize it once at the boundary and delete downstream special-casing.
- **Respect naming conventions for public-ish API**: if a type/symbol name can appear in downstream typings/exports, align with existing conventions and preserve backwards compatibility via explicit aliases.
- **Prefer semantically accurate names**: user-facing labels should reflect the underlying concept (don’t over-sell a `Thenable` as a `Promise` unless that’s actually what it is).

**Example patterns**
1) Rename without drift:
```js
// Before: expectedEnviromentName (typo) silently fell back via || 'Server'
expect(this.state.error.environmentName).toBe(
  this.props.expectedEnvironmentName || 'Server'
);
```
Then confirm the old misspelling no longer exists in the repo (e.g., grep/search).

2) Remove redundant event-prefix translation:
```js
// Instead of sprinkling checks for 'top' in many places,
// normalize once and pass canonical names downstream.
function topLevelTypeToEventName(topLevelType: string): string {
  return topLevelType.startsWith('top') ? topLevelType.slice(3).toLowerCase() : topLevelType;
}
```
(Or, better: don’t emit the `top`-prefixed form in the first place.)

3) Keep public export compatibility with aliases:
```js
export {Activity, Activity as unstable_Activity};
```

**Don’t**
- Let identifier spellings drift (typos + defaults can make tests “pass for the wrong reason”).
- Keep multiple ad-hoc translation layers for the same naming convention across modules.
- Rename semi-public types/symbols without considering downstream consumers and existing conventions.