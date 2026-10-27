---
title: Harden security boundaries
description: When code crosses trust boundaries (user input, serialized/deserialized
  data, error/debug surfaces, streamed DOM), enforce strict constraints and avoid
  leaking or inconsistently applying security-relevant metadata.
repository: facebook/react#b6
label: Security
language: JavaScript
comments_count: 7
repository_stars: 251888
---

When code crosses trust boundaries (user input, serialized/deserialized data, error/debug surfaces, streamed DOM), enforce strict constraints and avoid leaking or inconsistently applying security-relevant metadata.

**Apply these rules:**
1) **Validate at the input boundary.** Don’t rely only on UI hints—ensure only the intended characters can enter the value.
   - Example: for numeric-only fields, set an allowed pattern and still sanitize in the change handler.
   ```jsx
   <input
     type="text"
     inputMode="numeric"
     pattern="[0-9]*"
     aria-label="Result index"
     value={value}
     onChange={(e) => setValue(e.target.value.replace(/\D+/g, ''))}
   />
   ```
2) **Be conservative in production serialization/deserialization.** Only preserve/deserialize what you truly need; avoid leaking implementation details (error constructor names, `.cause`, debug payloads) in prod.
   - Practical pattern: gate any extra fields behind `__DEV__`, and ensure client logic mirrors what the server actually serialized.
3) **Use safe property traversal on untrusted object graphs.** When “drilling” into nested objects from serialized data, require own-properties so you don’t traverse unexpected structures.
   - Example:
   ```js
   const name = path[i];
   if (typeof value === 'object' && value !== null && Object.prototype.hasOwnProperty.call(value, name)) {
     value = value[name];
   } else {
     // stop / reject
   }
   ```
4) **Keep security attributes consistent (CSP nonce / integrity).** Don’t silently drop required attributes or merge DOM chunks when security metadata differs (e.g., different nonces). Prefer “known early” values or explicitly warn/reject incompatible combinations.
5) **Avoid `eval`/string-based execution when feasible; otherwise guard it tightly.** If tests require it, prefer using the actual provided APIs (e.g., `window.MutationObserver`) instead of `eval` strings, and ensure any eval-related behavior is checked/contained in the correct execution path.

Together, these practices reduce XSS-like gadget surfaces, information disclosure, inconsistent CSP bypass risk, and unsafe traversal of attacker-influenced object structures.