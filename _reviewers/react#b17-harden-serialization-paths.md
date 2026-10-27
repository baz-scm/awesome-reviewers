---
title: Harden serialization paths
description: 'When code serializes/deserializes, traverses object graphs, or uses
  debug-only dynamic execution, apply three safeguards:


  1) Guard object traversal with own-property checks'
repository: facebook/react#b17
label: Security
language: JavaScript
comments_count: 8
repository_stars: 251891
---

When code serializes/deserializes, traverses object graphs, or uses debug-only dynamic execution, apply three safeguards:

1) Guard object traversal with own-property checks
- Never assume traversed objects were created by your parser/serializer. Before reading nested properties, ensure the property is an own property.

2) Minimize production serialization surface and avoid leaking internals
- Don’t preserve/serialize sensitive error identity or extra fields (e.g., constructor names, Error.cause/details) in production if they aren’t needed. Keep such behavior dev-only.

3) Treat eval/debug/CSP/nonce behavior conservatively
- Prefer avoiding eval (including in test helpers). If eval is required for dev debugging, gate it behind __DEV__, explicitly detect CSP availability, and ensure CSP nonce handling is consistent (don’t merge/stream incompatible nonces).

Example (safe traversal + prod gating):
```js
function fulfillReference(response, reference, value) {
  const {path, handler} = reference;
  for (let i = 1; i < path.length; i++) {
    const key = path[i];
    // Prevent prototype/gadget drilling
    if (typeof value === 'object' && value !== null &&
        Object.prototype.hasOwnProperty.call(value, key)) {
      value = value[key];
    } else {
      // handle missing/invalid path safely
      return;
    }
  }
}

function serializeErrorForFlight(errorInfo) {
  // In prod, omit extra details/surface area
  if (!__DEV__) {
    return {message: 'An error occurred', /* digest only */};
  }
  // In dev, you may include richer diagnostics
  return {name: errorInfo.name, message: errorInfo.message, cause: errorInfo.cause};
}
```

Apply this standard to any code that (a) walks nested data from serialized streams, (b) reflects error identities/details, or (c) relies on dynamic execution and CSP-restricted behaviors (eval/nonce).