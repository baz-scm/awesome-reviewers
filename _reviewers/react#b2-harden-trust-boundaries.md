---
title: Harden trust boundaries
description: 'Apply a strict trust-boundary standard to security-sensitive code:


  - **Validate and constrain inputs**: Don’t rely on UI hints alone (e.g., `inputMode`).
  Enforce format via both UI attributes and parsing/sanitization. Example:'
repository: facebook/react#b2
label: Security
language: JavaScript
comments_count: 5
repository_stars: 251882
---

Apply a strict trust-boundary standard to security-sensitive code:

- **Validate and constrain inputs**: Don’t rely on UI hints alone (e.g., `inputMode`). Enforce format via both UI attributes and parsing/sanitization. Example:
  ```jsx
  <input
    type="text"
    inputMode="numeric"
    pattern="[0-9]*"
    onChange={(e)=>setValue(e.target.value.replace(/\D/g,''))}
  />
  ```
- **Defensively traverse objects**: When walking/serializing unknown objects or drilling through paths, require *own-property* checks to avoid gadget/probing/prototype surprises.
  ```js
  if (typeof value === 'object' && Object.prototype.hasOwnProperty.call(value, name)) {
    value = value[name];
  }
  ```
- **Don’t leak internal details in production**: Treat stack formatting, constructor names, or other implementation-specific identifiers as sensitive. Keep such fidelity behind `__DEV__` (or an equivalent), and in prod prefer generic messages.
- **Make thenable/promise assumptions explicit**: If values can come from userspace, guard against malicious behavior (e.g., resolving multiple times). If you truly control the thenables (vendored/owned implementation), document that assumption and still enforce invariants where feasible.
- **Use `eval` only with CSP-safe, non-silent handling**: If `eval` is required for dev tooling/debugging, ensure the availability check is co-located with the code that uses `eval`, report the caught error (not only a generic message), and fail in a controlled way when CSP blocks it.

Outcome: reduces XSS/data-exfil vectors, prevents object-walking gadget exploitation, avoids prod information leakage, and makes dynamic-execution paths auditable and CSP-compatible.