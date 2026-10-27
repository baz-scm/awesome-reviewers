---
title: Explicit API Contracts
description: 'When designing/adjusting public or semi-public APIs, make the contract
  explicit and spec-aligned: use an options bag (or schema object) instead of adding
  loosely related positional/optional flags; make parameter intent clear (either required
  or intentionally omitted—don’t silently default to `undefined`); ensure behavioral
  semantics match the authoritative...'
repository: facebook/react#b11
label: API
language: JavaScript
comments_count: 4
repository_stars: 251894
---

When designing/adjusting public or semi-public APIs, make the contract explicit and spec-aligned: use an options bag (or schema object) instead of adding loosely related positional/optional flags; make parameter intent clear (either required or intentionally omitted—don’t silently default to `undefined`); ensure behavioral semantics match the authoritative spec; and keep environment-specific transformations in the correct adapter/host layer.

Application guidelines:
- Prefer options bags for extensibility:
  - Bad: `getComponentByUid(uid, includeHooks?)`
  - Better: `getComponentByUid(uid, {includeHooks: true})`
- If a function/API takes cross-cutting request/init parameters (e.g., `integrity`, `fetchPriority`), either:
  - require them and let bindings map them, or
  - document exactly why/when they can be absent—avoid “sometimes undefined” without a contract.
- Match spec-defined identity/semantics precisely and lock with tests (especially when encoding/querying/normalizing options).
- Do not bake host-environment assumptions into shared library code (e.g., URL/sourcemap file-vs-fileURL); push those concerns into the host adapter.

Code sketch (options bag):
```ts
type GetComponentByUidOptions = {
  includeHooks?: boolean,
};

function getComponentByUid(uid: string, options: GetComponentByUidOptions = {}): NodeInfo | ToolError {
  const {includeHooks = false} = options;
  // ...
}
```