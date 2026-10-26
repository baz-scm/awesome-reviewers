---
title: Secure Input & CSP
description: 'Security-sensitive code should be hardened end-to-end: constrain inputs,
  safely traverse parsed/serialized objects, avoid leaking implementation details
  in production, and honor CSP (nonce) without relying on `eval`.'
repository: facebook/react#b3
label: Security
language: JavaScript
comments_count: 8
repository_stars: 251883
---

Security-sensitive code should be hardened end-to-end: constrain inputs, safely traverse parsed/serialized objects, avoid leaking implementation details in production, and honor CSP (nonce) without relying on `eval`.

**Apply these rules:**
1) **Constrain and validate inputs (don’t trust UI-only constraints).**
   - Use `inputMode`/`pattern` for UX, and also enforce the allowed character set in the change handler.
   - Example:
     ```jsx
     <input
       type="text"
       inputMode="numeric"
       pattern="[0-9]*"
       aria-label="Result index"
       value={value}
       onChange={e => {
         const digitsOnly = e.target.value.replace(/\D+/g, '');
         setValue(digitsOnly);
       }}
     />
     ```

2) **When walking objects/paths derived from parsing or remote data, guard property access.**
   - Use `Object.prototype.hasOwnProperty.call(obj, prop)` (or equivalent) before drilling.
   - Example:
     ```js
     const key = path[i];
     if (value !== null && typeof value === 'object' &&
         Object.prototype.hasOwnProperty.call(value, key)) {
       value = value[key];
     } else {
       // reject/stop
     }
     ```

3) **Avoid leaking implementation details in production errors/serialization.**
   - Keep “rich” error fidelity (names/constructors, debug fields like `cause`) behind `__DEV__`.
   - Don’t preserve constructor names or include sensitive message details in prod error outputs.

4) **Respect CSP and minimize `eval`.**
   - Prefer native APIs (e.g., `new window.MutationObserver(...)`) over `eval`.
   - If `eval` is unavoidable for dev tooling, handle CSP failures safely and include the underlying error details in logs.

5) **Propagate CSP nonces consistently and don’t merge outputs across different nonces.**
   - If you emit/merge inline `<style>` content, ensure the merged output does not combine rules with different `nonce` values; require `nonce` to be known at the right time (or segregate by nonce).

Following these practices reduces the risk of XSS/input abuse, prototype/gadget traversal issues, and inadvertent information disclosure while keeping CSP protections effective.