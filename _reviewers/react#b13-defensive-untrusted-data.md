---
title: Defensive Untrusted Data
description: 'When processing serialized or otherwise untrusted data across trust
  boundaries (e.g., Flight references, error serialization/deserialization), apply
  “defensive boundaries”:'
repository: facebook/react#b13
label: Security
language: JavaScript
comments_count: 4
repository_stars: 251893
---

When processing serialized or otherwise untrusted data across trust boundaries (e.g., Flight references, error serialization/deserialization), apply “defensive boundaries”:

1) Restrict object traversal to safe keys
- Before drilling into nested structures from an encoded reference, only traverse *own properties* of objects produced by the parser.
- Use `Object.prototype.hasOwnProperty.call(obj, key)` (or recreate with a null-prototype) instead of assuming normal objects are safe.

2) Avoid information leaks via prod error payloads
- Don’t preserve or deserialize implementation-specific error details (constructor name, custom `Error.name`, stack variants, `Error.cause`, etc.) in production if the server doesn’t intentionally serialize them.
- Gate sensitive fields with `__DEV__` and treat “unexpected fields in prod” as defense-in-depth.

3) Keep dev-only security instrumentation deterministic
- If you use tainting or debug-only instrumentation, ensure its lifecycle/cleanup is ordered so production semantics remain correct and so debug instrumentation doesn’t inadvertently change resource management or subsequent flush behavior.

Example (own-property guard + prod/dev error field gating):
```js
function fulfillReference(value, reference) {
  const name = reference.path[i];
  if (typeof value === 'object' &&
      value !== null &&
      Object.prototype.hasOwnProperty.call(value, name)) {
    value = value[name];
  } else {
    // stop or reject
  }
}

function resolveErrorDev(errorInfo) {
  const errorOptions =
    // Only deserialize fields we know are serialized in DEV.
    __DEV__ && ('cause' in errorInfo);
  // ...construct error safely
}
```