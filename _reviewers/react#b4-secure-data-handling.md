---
title: Secure Data Handling
description: 'Treat all externally influenced values (user input, serialized error
  objects, dynamically walked object graphs, and security attributes like CSP nonces)
  as untrusted. Enforce three rules:'
repository: facebook/react#b4
label: Security
language: JavaScript
comments_count: 7
repository_stars: 251885
---

Treat all externally influenced values (user input, serialized error objects, dynamically walked object graphs, and security attributes like CSP nonces) as untrusted. Enforce three rules:

1) Canonicalize and validate inputs before use
- For numeric fields, don’t rely on UI hints alone; also validate and strip/convert on change.
- Consider using inputMode/pattern for UX, but ensure the handler guarantees the stored value is the canonical safe form.

2) Don’t leak implementation details in production
- In prod, avoid preserving or exposing sensitive error specifics (e.g., custom constructor names) and avoid serializing/deserializing fields you said you wouldn’t.
- Use defense-in-depth: gate optional/sensitive deserialization paths (e.g., Error.cause-like fields) behind __DEV__ when you never serialize them in prod.

3) Harden dynamic traversal against prototype/gadget attacks
- When walking objects derived from parsing/transport, only access own properties.
- Prefer explicit own-property checks (or null-prototype reconstruction) before drilling into nested values.

4) Keep security attributes correct and consistent (CSP nonces, integrity)
- Ensure CSP nonces are known early enough for inline security-sensitive output.
- Never merge content generated under different security contexts (e.g., style tags with different nonces) into a single output that could break CSP or weaken enforcement.

Example pattern (combining the key checks):
```js
function onDigitInputChange(e) {
  // Canonicalize: store digits only
  const digitsOnly = e.target.value.replace(/\D+/g, '');
  setValue(digitsOnly);
}

function safeDrill(value, path) {
  for (let i = 0; i < path.length; i++) {
    const key = path[i];
    // Harden traversal: only traverse own properties
    if (value !== null && typeof value === 'object' &&
        Object.prototype.hasOwnProperty.call(value, key)) {
      value = value[key];
    } else {
      return undefined;
    }
  }
  return value;
}

function resolveErrorForProd(err) {
  // Avoid leaking custom error constructor/name/details in prod
  if (!__DEV__) return {message: 'An error occurred'};
  return {name: err.name, message: err.message};
}
```

Use this standard whenever code:
- Accepts or stores user input,
- Serializes/deserializes error/graph data,
- Traverses parsed objects dynamically,
- Emits security-relevant markup (CSP nonces, integrity-bearing links/scripts).