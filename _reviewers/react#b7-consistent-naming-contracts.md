---
title: Consistent Naming Contracts
description: 'Treat naming as a compatibility contract and enforce consistency.


  Apply this when adding/changing identifiers, exported types, flags, props, or user-facing
  labels:'
repository: facebook/react#b7
label: Naming Conventions
language: JavaScript
comments_count: 6
repository_stars: 251888
---

Treat naming as a compatibility contract and enforce consistency.

Apply this when adding/changing identifiers, exported types, flags, props, or user-facing labels:
1) **No typos in identifiers**: after a rename, confirm all call sites use the new spelling. Do a repo-wide search for both the old and new names to avoid “it still works due to defaults” situations.
2) **Follow existing naming conventions**: match established patterns (prefix/suffix rules like `*Options`, flag naming, etc.) instead of introducing one-off variants.
3) **For semi-public/public surface, preserve compatibility**: if consumers may use old names, provide aliases rather than removing/renaming abruptly.
4) **Centralize naming transformations**: don’t replicate the same “rename/prefix-strip” logic in many places—make the naming scheme consistent at the source so downstream code is simpler.

Example (compatibility alias):
```js
// New canonical name
export { Activity, Activity as unstable_Activity };
```

Example (rename safety):
```js
// Before rename, ensure old spelling isn’t still referenced elsewhere:
// expectedEnviromentName  (old)
// expectedEnvironmentName (new)
// Don’t rely on fallbacks like `|| 'Server'` to hide mismatches.
```