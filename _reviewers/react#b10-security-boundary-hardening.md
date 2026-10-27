---
title: Security Boundary Hardening
description: 'When code crosses security boundaries (user input, parsed/serialized
  data, deep object traversal, dynamic rendering under CSP, or error reporting), harden
  it explicitly: '
repository: facebook/react#b10
label: Security
language: JavaScript
comments_count: 7
repository_stars: 251894
---

When code crosses security boundaries (user input, parsed/serialized data, deep object traversal, dynamic rendering under CSP, or error reporting), harden it explicitly: 

- **Validate and normalize inputs at the edge**: use both declarative constraints and runtime normalization so the value is always in the expected form.
  ```jsx
  <input
    type="text"
    inputMode="numeric"
    pattern="[0-9]*"
    value={value}
    onChange={e => setValue(e.target.value.replace(/\D/g, ''))}
  />
  ```

- **Avoid leaking internal details in production**: in `__DEV__` you can preserve richer error metadata, but in production avoid preserving custom constructor/name/stack details that could reveal implementation details.

- **Prevent unsafe deep traversal**: when walking objects from parsers/untrusted sources, only traverse **own properties** (not inherited/prototype/gadget properties).
  ```js
  const name = path[i];
  if (typeof value === 'object' && value !== null &&
      Object.prototype.hasOwnProperty.call(value, name)) {
    value = value[name];
  }
  ```

- **Be intentional with `eval()` and CSP**:
  - Prefer non-`eval` solutions (e.g., the correct `window.MutationObserver` type instead of eval’ing a string).
  - If `eval()` is unavoidable, never silently swallow unexpected failures—log the caught error and ensure the behavior aligns with CSP expectations.

- **Propagate CSP nonces correctly**: require and thread nonce values consistently through streaming rendering paths; don’t merge/compose style chunks that may carry incompatible nonces (otherwise you risk CSP violations or incorrect security attributes).

Adopt this as a standard checklist: **(1) constrain + normalize inputs, (2) guard deep traversal with own-property checks, (3) redact sensitive production errors, (4) minimize/contain eval, (5) ensure CSP nonce consistency.**