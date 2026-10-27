---
title: Naming Conventions Enforcement
description: 'Apply a consistent naming standard as a compatibility contract.


  Checklist for changes that touch identifiers (props, exported APIs, types, flags,
  and devtools labels):'
repository: facebook/react#b9
label: Naming Conventions
language: JavaScript
comments_count: 7
repository_stars: 251891
---

Apply a consistent naming standard as a compatibility contract.

Checklist for changes that touch identifiers (props, exported APIs, types, flags, and devtools labels):
1) **Follow the existing convention** for the name’s “namespace” (e.g., `XOptions` for option types; static-vs-render flag suffix patterns).
2) **Centralize naming transforms**—don’t reimplement the same naming convention/prefix-removal logic in many places.
3) **Treat public/semi-public names as stable**: if you must rename, **preserve backward compatibility** with explicit aliases (e.g., export both the new name and the old name mapped to it).
4) **Audit for lingering typos/old spellings** across the repo; otherwise changes can “pass” via fallbacks and hide incorrect wiring.
5) **For user-facing/devtools output, use the existing naming strategy** (prefer the conventional dominant label unless there’s a strong reason otherwise).

Example (aliasing for compatibility):
```js
// New canonical export
export {Activity};
// Back-compat alias
export {Activity as unstable_Activity};
```

Example (typo audit mindset):
- If you rename `expectedEnviromentName` → `expectedEnvironmentName`, do a repo-wide search for the old misspelling before merge to avoid silent fallback defaults.