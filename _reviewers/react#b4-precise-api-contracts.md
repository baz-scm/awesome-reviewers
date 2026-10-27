---
title: Precise API Contracts
description: 'When defining or changing an API contract—whether it’s a public option
  or a modeled function signature—treat it as an explicit behavioral contract:


  1) Encode semantics precisely'
repository: facebook/react#b4
label: API
language: TypeScript
comments_count: 4
repository_stars: 251885
---

When defining or changing an API contract—whether it’s a public option or a modeled function signature—treat it as an explicit behavioral contract:

1) Encode semantics precisely
- Ensure the declared parameter/effect modeling matches the real behavior of the method, especially which inputs are stored/captured vs only read.
- Example (modeled `fill(value, start, end)`):
  ```ts
  // fill(value, start, end): value is stored into the array
  // while the other args are only read
  {
    positionalParams: [Effect.Capture],
    restParam: Effect.Read,
  }
  ```
- Example (modeled `with(index, value)`):
  ```ts
  // with(index, value): index is read, value is captured/stored
  {
    positionalParams: [Effect.Read, Effect.Capture],
  }
  ```

2) Preserve compatibility: deprecate before removing
- If an option/feature has any external surface area (even if undocumented or debatable), prefer marking it deprecated and keeping it working until a planned removal window.
- Only remove outright when you can clearly justify it as non-breaking (or it’s already communicated/expected).

3) Keep internal contracts minimal
- If a function/object already has access to needed context, don’t thread redundant parameters through the call chain.
- Prefer using existing context over expanding function signatures just to pass information that’s already reachable.