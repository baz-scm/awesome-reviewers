---
title: Spec-Accurate API Contracts
description: 'Design API surfaces so callers get clear, contract-correct behavior
  across environments.


  Apply these rules:

  1) Fail fast on invalid context (avoid permissive no-ops). If an API is server-only,
  don’t export a browser-safe stub—make client imports throw (or resolve to a compile-time/runtime
  error) so misuse is caught early.'
repository: facebook/react#b4
label: API
language: JavaScript
comments_count: 6
repository_stars: 251885
---

Design API surfaces so callers get clear, contract-correct behavior across environments.

Apply these rules:
1) Fail fast on invalid context (avoid permissive no-ops). If an API is server-only, don’t export a browser-safe stub—make client imports throw (or resolve to a compile-time/runtime error) so misuse is caught early.
2) Use explicit, schema-aligned API shapes. Prefer an options bag (typed object) over adding loosely related optional positional parameters, especially for public tool interfaces.
3) Match the underlying external contract/spec for semantics. If the platform defines identity keys or required enum/string values, encode that exactly; don’t rely on approximate behavior.
4) Keep public types truthful. If a field may not be present, make it optional in the exported type; ensure enum/string mappings are correct.
5) Avoid signature “mode explosion.” If behavior diverges by distinct variants, split into separate functions/constructors or accept a structured variant object instead of accumulating many mode parameters.

Example (server-only API should error in client context rather than no-op):
```js
// server-only module
export function createMaskLedger() {
  if (typeof window !== 'undefined') {
    throw new Error('createMaskLedger is server-only; import it only in server code');
  }
  // ...real implementation...
}

export function addToLedger() {
  if (typeof window !== 'undefined') {
    throw new Error('addToLedger is server-only; import it only in server code');
  }
  // ...real implementation...
}
```