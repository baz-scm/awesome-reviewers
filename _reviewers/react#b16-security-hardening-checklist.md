---
title: Security Hardening Checklist
description: 'When building features that touch untrusted data, dynamic environments,
  or security-sensitive output, apply these rules:


  1) Constrain inputs at the boundary'
repository: facebook/react#b16
label: Security
language: JavaScript
comments_count: 8
repository_stars: 251891
---

When building features that touch untrusted data, dynamic environments, or security-sensitive output, apply these rules:

1) Constrain inputs at the boundary
- Use both UI constraints and handler-side normalization.
- Example (digits-only field):
  ```jsx
  <input
    type="text"
    inputMode="numeric"
    pattern="[0-9]*"
    onChange={e => {
      const digitsOnly = e.target.value.replace(/\D/g, '');
      setValue(digitsOnly);
    }}
  />
  ```

2) Harden any object traversal against unexpected properties
- When drilling into objects derived from parsing/remote data, only follow own-properties.
  ```js
  if (typeof value === 'object' && value !== null) {
    if (Object.prototype.hasOwnProperty.call(value, name)) {
      value = value[name];
    }
  }
  ```

3) Treat error/debug details as sensitive in production
- Avoid preserving internal constructor names, stack specifics, or debug info in prod unless explicitly required.
- Prefer DEV-only behavior when improving diagnosis.

4) Respect CSP nonces consistently in streamed/emitted markup
- If you rely on CSP nonces to allow React-emitted scripts, ensure the nonce is provided to the streaming entrypoint.
- Ensure merged/combined resources don’t silently combine different nonces; keep nonce consistency per emitted tag.

5) Minimize `eval`/dynamic code execution and don’t swallow security diagnostics
- Prefer using the correct runtime APIs (e.g., `new window.MutationObserver(...)`) over `eval`-string workarounds.
- If capability probing is necessary, include the caught error details in logs so failures aren’t silently misclassified.

Applying these consistently reduces injection risk, gadget-style traversal bugs, accidental information disclosure, and CSP-related security regressions.