---
title: Explicit API Contracts
description: When designing or evolving API surfaces (function interfaces, host/tool
  lists, REST/WebSocket payloads, and request headers), make the contract unambiguous
  and single-sourced.
repository: CLINE/CLINE
label: API
language: TypeScript
comments_count: 4
repository_stars: 70837
---

When designing or evolving API surfaces (function interfaces, host/tool lists, REST/WebSocket payloads, and request headers), make the contract unambiguous and single-sourced.

Apply these rules:
1) Replace positional booleans with named options
- Prefer `load({ refresh: true, userInitiated: true })` over `load(true, true)`.
- Use destructuring defaults:
```ts
function load(args: { refresh?: boolean; userInitiated?: boolean } = {}) {
  const { refresh = false, userInitiated = false } = args;
  // ...
}
```

2) Don’t “almost” follow the spec—encode it unconditionally
- If a spec says the host MUST NOT list tools whose visibility doesn’t include `"model"`, implement the visibility filter without exceptions tied to unrelated flags.
- If you need a feature gate, ensure it changes only what the spec allows—not the meaning of required filtering.

3) Keep field/header names semantically aligned with their values
- Never change a request header’s meaning while leaving the header name unchanged (e.g., sending `ulid` in `X-Task-ID`).
- If the value type/meaning changes, rename the header or send both identifiers as separate, clearly named fields.

4) Avoid duplicated readiness/config flags
- Don’t store “derived readiness” in multiple layers unless you can guarantee synchronization.
- Prefer reading the readiness from the shared contract/metadata and propagate it through the API directly.

These changes prevent silent behavior changes, reduce call-site confusion, and keep client/server integration stable as the codebase evolves.