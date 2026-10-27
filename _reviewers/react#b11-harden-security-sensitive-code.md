---
title: Harden security sensitive code
description: 'When code touches security boundaries (user input, dynamic execution,
  object graph traversal, error reporting, or CSP/nonce-based rendering), apply defense-in-depth:
  validate/normalize, prevent unintended traversal, avoid leaking details, handle
  dangerous APIs safely, and ensure CSP nonces are consistent.'
repository: facebook/react#b11
label: Security
language: JavaScript
comments_count: 6
repository_stars: 251894
---

When code touches security boundaries (user input, dynamic execution, object graph traversal, error reporting, or CSP/nonce-based rendering), apply defense-in-depth: validate/normalize, prevent unintended traversal, avoid leaking details, handle dangerous APIs safely, and ensure CSP nonces are consistent.

Checklist:
1) Constrain & normalize inputs
- Prefer client-side constraints (e.g., numeric `inputMode`, `pattern`) but also enforce server/handler-side normalization so the value cannot contain unexpected characters.

2) Guard all property/path traversal
- When walking objects by dynamic keys/paths, only traverse own properties (and avoid prototype surprises).

3) Prevent sensitive info disclosure
- In production, don’t preserve or expose implementation-specific error metadata (e.g., original constructor names) if it could leak details.

4) Treat `eval` (and similar) as hazardous
- Explicitly distinguish “not available”/CSP-restricted cases from other failures; log enough diagnostic context without swallowing unexpected errors silently.

5) Enforce CSP nonce compatibility
- If you cache or merge rendered resources (e.g., styles), only reuse when the effective nonce matches; otherwise keep them separate (or warn in dev).

Example patterns:
```js
// (1) Constrain + normalize
<input
  inputMode="numeric"
  pattern="[0-9]*"
  onChange={(e) => {
    const digitsOnly = e.target.value.replace(/\D+/g, '');
    // setState(digitsOnly)
  }}
/>

// (2) Guard property traversal
function safeDrill(value, key) {
  if (value !== null && typeof value === 'object' &&
      Object.prototype.hasOwnProperty.call(value, key)) {
    return value[key];
  }
  return undefined;
}

// (3) Dev-only detailed error
const displayed = __DEV__ ? error.stack : 'A generic error occurred.';

// (4) eval handling
try {
  (0, eval)('null');
} catch (error) {
  console.error('eval() unavailable or blocked.', error);
}

// (5) nonce-aware merge decision
function canMergeStyle(prevNonce, nextNonce) {
  return prevNonce === nextNonce;
}
```