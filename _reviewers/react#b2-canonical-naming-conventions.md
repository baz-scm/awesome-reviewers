---
title: Canonical Naming Conventions
description: Use a single, canonical spelling/labeling scheme for any externally-observed
  identifier (props, event names, exported APIs, public/semi-public types/options,
  user-facing labels). Avoid proliferating alternate names or ad-hoc conversions.
repository: facebook/react#b2
label: Naming Conventions
language: JavaScript
comments_count: 7
repository_stars: 251882
---

Use a single, canonical spelling/labeling scheme for any externally-observed identifier (props, event names, exported APIs, public/semi-public types/options, user-facing labels). Avoid proliferating alternate names or ad-hoc conversions.

Apply this checklist:
1) **No typos in identifier contracts:** If you rename a prop/type/export for correctness, verify the old spelling is fully removed (e.g., repo-wide search) to prevent silent fallback behavior.
2) **Single source of truth for name mapping:** Don’t duplicate “name translation” logic in many places. Prefer converting at the source (or centralizing in one helper) so downstream code consumes the canonical form.
3) **Follow existing naming conventions for contract-adjacent symbols:**
   - For options types, match the established pattern used across the codebase.
   - For enumerated flags, preserve established suffix/prefix conventions (e.g., render-specific vs static).
   - For public/stable vs unstable API exports, preserve compatibility with explicit aliases.
4) **Keep naming semantics honest:** Don’t let examples imply a specific domain (e.g., treating arbitrary strings as “paths”) if the consumer shouldn’t assume that.
5) **User-facing labels should match the dominant mental model:** When choosing between terms like “Thenable” vs “Promise”, prefer the naming logic used elsewhere in the codebase so UI output stays consistent with expectations.

Example (centralize event-name conversion):
```js
// Canonical: downstream code should deal only with the converted name.
export function topLevelTypeToEventName(topLevelType) {
  return topLevelType.startsWith('top')
    ? topLevelType.slice(3).toLowerCase()
    : topLevelType;
}

// Use this once at the boundary instead of re-implementing conversions everywhere.
const eventName = topLevelTypeToEventName(nativeEvent.topLevelType);
```