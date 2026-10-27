---
title: Harden CSP and Gadgets
description: 'In security-sensitive code paths (streaming/serialization, debug instrumentation,
  and anything that affects CSP), apply four rules:


  1) Prevent production info leaks'
repository: facebook/react#b9
label: Security
language: JavaScript
comments_count: 6
repository_stars: 251891
---

In security-sensitive code paths (streaming/serialization, debug instrumentation, and anything that affects CSP), apply four rules:

1) Prevent production info leaks
- Never preserve or expose debug/internal details (e.g., constructor names, debug chunks) in production outputs.
- Gate any “preserve name / include debug info” behavior behind `__DEV__`.

2) Make dynamic execution CSP-aware and failure-transparent
- If you must use `eval`-like functionality, first check availability in dev, and in failures log the caught error (don’t swallow it). Example:

```js
let hasConfirmedEval = false;
export function checkEvalAvailabilityOnceDev(): void {
  if (__DEV__ && !hasConfirmedEval) {
    hasConfirmedEval = true;
    try {
      (0, eval)('null');
    } catch (error) {
      console.error(
        'eval() not supported (likely CSP missing unsafe-eval).',
        error,
      );
    }
  }
}
```

3) Safely traverse parsed objects
- When “drilling” through structured data, only follow properties that are owned by the object created by your parser. Always use own-property guards when walking values.

```js
const name = path[i];
if (value !== null && typeof value === 'object' &&
    Object.prototype.hasOwnProperty.call(value, name)) {
  value = value[name];
}
```

4) Propagate CSP nonces consistently
- Treat CSP nonce as part of the rendering/security contract: ensure it’s known and used consistently for the produced tags/queues.
- Don’t merge/aggregate style/script output across different nonces; if nonce can differ, keep nonce-specific rendering separate (or warn in dev when inconsistent).

Applying these rules reduces the risk of prototype/gadget traversal, CSP breakage, and unintended disclosure of internal/debug information.