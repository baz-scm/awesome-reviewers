---
title: Harden data boundaries
description: 'Apply consistent security hardening whenever code ingests, traverses,
  or re-serializes potentially untrusted data.


  **Rules**

  - **Traversal:** When drilling into objects/structures that originated outside your
  own parser/runtime, only access **own properties**. Never assume inherited/proxied
  properties are safe.'
repository: facebook/react#b5
label: Security
language: JavaScript
comments_count: 6
repository_stars: 251886
---

Apply consistent security hardening whenever code ingests, traverses, or re-serializes potentially untrusted data.

**Rules**
- **Traversal:** When drilling into objects/structures that originated outside your own parser/runtime, only access **own properties**. Never assume inherited/proxied properties are safe.
- **Prod vs dev leakage:** Don’t serialize/propagate implementation details (error constructor names, `Error.cause`, etc.) in production unless there’s a deliberate, documented reason.
- **Security invariants:** For CSP-related rendering, keep security-relevant attributes consistent (e.g., don’t merge inline styles if nonces differ).
- **Validation/escaping:** Enforce input invariants at the boundary (e.g., digits-only) and escape output for the exact context (e.g., `Link` header escaping between `<` and `>`).
- **Avoid dynamic execution when possible:** Prefer non-`eval` APIs; if `eval` is unavoidable for dev/test, ensure it’s localized and dev-gated.

**Example (own-property guard during traversal)**
```js
function safeDrill(value, path) {
  for (let i = 0; i < path.length; i++) {
    const key = path[i];
    if (typeof value === 'object' && value !== null) {
      if (!Object.prototype.hasOwnProperty.call(value, key)) return null;
      value = value[key];
    } else {
      return null;
    }
  }
  return value;
}
```

Use this checklist for any code paths involving parsing of remote/serialized data, error reconstruction, CSP nonce/streaming output, or security-header generation.