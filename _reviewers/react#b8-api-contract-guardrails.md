---
title: API Contract Guardrails
description: When an API surface has different valid contexts (e.g., server vs client)
  or must interoperate with a platform contract (e.g., preload/link semantics, tool
  argument schemas), make the contract explicit and fail fast.
repository: facebook/react#b8
label: API
language: JavaScript
comments_count: 4
repository_stars: 251889
---

When an API surface has different valid contexts (e.g., server vs client) or must interoperate with a platform contract (e.g., preload/link semantics, tool argument schemas), make the contract explicit and fail fast.

Apply these rules:
1) Fail fast on invalid context
- Do not export server-only helpers into client bundles as no-ops.
- Instead, ensure client imports/usage throw with a clear error message so developers get immediate feedback.

2) Prefer schema-stable argument shapes
- When adding optional behavior to tool/function APIs, use an options bag (object arguments) aligned with the public tool input schema, rather than adding new positional booleans.

3) Normalize required parameters; never “undefined by accident”
- Treat required external/platform parameters as part of the API contract.
- Have adapters/bindings decide values, but avoid silently weakening the contract by passing undefined where a defined contract exists.

4) Validate outbound parameter values against the external API spec
- Ensure identifiers/enum values passed to platform APIs are correct (e.g., preload rel values).
- Add tests for the exact contract mapping so incorrect strings don’t ship.

Example (options bag + fail-fast pattern):
```js
// Client-facing entry: fail fast if a server-only API is imported.
export function addToLedger() {
  throw new Error('addToLedger is server-only; do not import it from client components.');
}

// Schema-stable tool signature: object arguments with named keys.
export function getComponentByUid({ uid, includeHooks = false }) {
  // ...
}
```

These guardrails keep API behavior correct across environments, reduce silent semantic drift, and make integrations (including DevTools/public tooling and platform bindings) more predictable.