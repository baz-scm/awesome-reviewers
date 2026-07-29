---
title: Explicit Null Semantics
description: When handling optional/nullable values in TypeScript/React, make “unset/default”
  distinct from “legitimate empty/zero” and avoid truthiness-based guards.
repository: aaif-goose/goose
label: Null Handling
language: TSX
comments_count: 4
repository_stars: 51876
---

When handling optional/nullable values in TypeScript/React, make “unset/default” distinct from “legitimate empty/zero” and avoid truthiness-based guards.

Apply:
1) Use a dedicated sentinel for “never set”
- Prefer `null`/`undefined` to represent “unset”, especially when `0`, `''`, or `false` are meaningful.
2) Check explicitly for sentinel/optionals
- Prefer `value !== undefined` / `value != null` over `if (value)` when the value may be `0` or `''`.
3) Normalize before branching
- For user input, normalize (`trim`) before deciding which code path applies.
4) Validate using the intended combined condition
- Compute derived state first, then apply the combined predicate.

Example (sentinel + explicit checks):

```ts
// Sentinel models “never set” separately from a real 0.
const [navExpandedWidth, setNavExpandedWidth] = useState<number | null>(null);

useEffect(() => {
  window.electron.getSetting('navExpandedWidth').then((stored: number | null) => {
    if (stored === null) {
      // keep component default
      return;
    }

    // stored === 0 is a legitimate explicit value, not “unset”
    setNavExpandedWidth(stored);
  });
}, []);

// Explicit optional check (don’t rely on truthiness)
const initialMessage = editedMessage !== undefined
  ? { msg: editedMessage, images: [] }
  : undefined;
```

This prevents bugs where guards accidentally skip applying valid persisted values (e.g., `0`) or mis-handle empty-but-present content (e.g., `''`).