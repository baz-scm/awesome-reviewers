---
title: Contract-First API Design
description: When designing any public/consumer-facing API (including devtools tools,
  server/client boundaries, and types reflected to users), treat the API contract
  as the source of truth and make misuse or mismatch fail fast.
repository: facebook/react#b5
label: API
language: JavaScript
comments_count: 5
repository_stars: 251886
---

When designing any public/consumer-facing API (including devtools tools, server/client boundaries, and types reflected to users), treat the API contract as the source of truth and make misuse or mismatch fail fast.

Apply this checklist:
1) Enforce context/environment correctness
- If an API is server-only (or otherwise context-specific), don’t provide silent client fallbacks.
- Prefer: do not export from client builds, or make importing/using it in the wrong context throw/produce an early error.

2) Match the external schema with the input shape
- If the consumer contract expects an “arguments object” (keyed parameters), expose an options bag rather than positional/alternating parameters.
- Keep the argument keys stable to avoid breaking downstream schema validation.

3) Make requiredness/optional fields intentional
- Parameters and public reflected fields should be optional only when the implementation truly may omit them.
- If the API intends callers to control a value (e.g., integrity/fetchPriority), encode that as required in the interface and let bindings decide what to pass when applicable.

4) Use types that encode assignability correctly
- For generic public types, choose variance and defaults that match real usage so assignment/compatibility is predictable.

Example (options bag + contract-aligned signature):
```js
// Prefer keyed options when the contract expects argument objects.
export type GetComponentArgs = {
  uid: string,
  includeHooks?: boolean,
};

export function getComponentByUid(args: GetComponentArgs): NodeInfo | ToolError {
  const {uid, includeHooks = false} = args;
  // ...
}

// Server-only API: fail fast in the wrong context.
export function createMaskLedger() {
  throw new Error('createMaskLedger is server-only and cannot be used in client components.');
}
```