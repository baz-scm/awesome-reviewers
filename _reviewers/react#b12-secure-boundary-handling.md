---
title: Secure boundary handling
description: 'Apply a single standard to security-sensitive code paths: validate/sanitize
  external inputs early, harden object traversal against unexpected shapes, enforce
  CSP requirements (nonces) consistently, strictly limit `eval` usage to controlled
  dev/test scenarios, and avoid leaking implementation details in production.'
repository: facebook/react#b12
label: Security
language: JavaScript
comments_count: 7
repository_stars: 251896
---

Apply a single standard to security-sensitive code paths: validate/sanitize external inputs early, harden object traversal against unexpected shapes, enforce CSP requirements (nonces) consistently, strictly limit `eval` usage to controlled dev/test scenarios, and avoid leaking implementation details in production.

How to apply:
- Input validation: constrain user-controlled fields at both the UI and data-handling layers (e.g., use `inputMode` + `pattern`, and also strip to the allowed character set in the change handler).
- Safe traversal: when iterating/drilling into parsed/derived objects, only traverse own properties; never assume arbitrary objects have safe shapes.
- CSP nonce correctness: when emitting nonceable tags (like inline `<style>`), propagate the nonce used by the stream/render context, and avoid merging/rendering outputs that would combine content protected by different nonces.
- `eval` control: keep `eval` strictly behind dev/test flags; if used, log meaningful error details (including the caught error) and prefer non-`eval` alternatives when possible.
- Production error leakage: don’t preserve or expose internal constructor names/details in production outputs; normalize errors so they don’t reveal implementation specifics.

Example patterns:
```js
// 1) Validate input (UI + handler)
<input
  type="text"
  inputMode="numeric"
  pattern="[0-9]*"
  aria-label="Result index"
/>

function onChange(e) {
  e.target.value = e.target.value.replace(/\D/g, '');
}

// 2) Harden traversal
if (typeof value === 'object' && value !== null && Object.prototype.hasOwnProperty.call(value, name)) {
  value = value[name];
}

// 3) Production error normalization
function serializeError(err) {
  return {
    message: __DEV__ ? String(err && err.message) : 'An error occurred in production.',
    // omit constructor/name/details in production
  };
}
```

If these practices are followed consistently, you reduce risk of injection, prototype/gadget exploitation during parsing, CSP bypass via incorrect nonce handling, and unintended information disclosure through errors or debugging utilities.