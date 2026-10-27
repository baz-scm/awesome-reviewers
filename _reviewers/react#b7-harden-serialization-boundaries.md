---
title: Harden serialization boundaries
description: When implementing Flight/serialization/debug plumbing, treat parsing
  traversal, emitted error/stack details, and any eval/CSP behavior as security boundaries.
repository: facebook/react#b7
label: Security
language: JavaScript
comments_count: 5
repository_stars: 251888
---

When implementing Flight/serialization/debug plumbing, treat parsing traversal, emitted error/stack details, and any eval/CSP behavior as security boundaries.

**Standards**
1) **Constrain object traversal to parser-owned properties**: when walking arbitrary values/paths, only traverse *own* properties of plain objects.
2) **Prevent production leakage**: do not preserve or serialize constructor-specific/internal details (e.g., custom `Error` names/constructors) in production outputs.
3) **Make CSP/eval failures safe and diagnosable**: keep `eval` strictly DEV-only, ensure the availability check is colocated with the code that calls `eval`, and when catching errors include the thrown error in logs.
4) **Scope debug instrumentation cleanup**: ensure security-related debug mechanisms (e.g., taint tracking) are cleaned up in the correct lifecycle window so they can’t affect non-debug output.

**Example patterns**
```js
// 1) Safe traversal: own-property only
const name = path[i];
if (value !== null && typeof value === 'object' && Object.prototype.hasOwnProperty.call(value, name)) {
  value = value[name];
}

// 2) Production-safe error details
function renderErrorForOutput(err) {
  if (!__DEV__) {
    return 'An error occurred'; // omit constructor/name/details
  }
  return err.stack; // DEV only
}

// 3) DEV-only eval + informative logging
let hasConfirmedEval = false;
export function checkEvalAvailabilityOnceDev() {
  if (__DEV__ && !hasConfirmedEval) {
    hasConfirmedEval = true;
    try {
      // eslint-disable-next-line no-eval
      (0, eval)('null');
    } catch (error) {
      console.error('eval() blocked by environment/CSP or other error:', error);
    }
  }
}
```

Applying these rules reduces risks from gadget/probing via unsafe traversal, prevents sensitive detail leakage, and ensures CSP-related issues don’t silently fail or create misleading security assumptions.