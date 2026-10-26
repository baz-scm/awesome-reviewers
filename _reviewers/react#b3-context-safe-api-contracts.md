---
title: Context-Safe API Contracts
description: 'Design APIs so their contracts are explicit, structured, and safe in
  the right execution context.


  - **Fail fast on invalid context**: If an API is server-only (or otherwise context-restricted),
  don’t export silent no-ops to the wrong runtime. Instead, make misuse an error so
  developers get immediate feedback.'
repository: facebook/react#b3
label: API
language: JavaScript
comments_count: 4
repository_stars: 251883
---

Design APIs so their contracts are explicit, structured, and safe in the right execution context.

- **Fail fast on invalid context**: If an API is server-only (or otherwise context-restricted), don’t export silent no-ops to the wrong runtime. Instead, make misuse an error so developers get immediate feedback.
- **Use schema-aligned argument objects**: For public/tooling APIs, prefer an **options bag / argument object** over positional parameters, matching any external schema expectations (e.g., “arguments as keys”).
- **Make variants readable**: If an API grows multiple modes/variants, don’t hide them behind many flat parameters. Prefer **separate functions per variant** or **nested option objects** that reflect meaning (so downstream logic and checks stay unambiguous).
- **Stay spec-correct**: When encoding behavior that depends on platform rules/identity semantics, derive values to match the platform spec (avoid “close enough” identity keys).

Example (shape + variant clarity):
```js
// Prefer structured options instead of many positional flags.
function createResponseState(options) {
  // options = { mode: 'fallback', bootstrapScriptContent, ... }
  // Resolve options to a single internal representation here.
}

// Prefer context-safe exports: server-only APIs should error when imported/used in a client runtime.
export function createMaskLedger() {
  if (isClientRuntime()) {
    throw new Error('createMaskLedger is server-only');
  }
  // ...server implementation...
}
```