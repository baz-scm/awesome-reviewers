---
title: Security Hardening Checklist
description: 'Apply this rule to code paths that handle user-controlled data, parsed
  objects, or runtime environments:


  1) Validate/whitelist inputs at multiple layers'
repository: facebook/react#b15
label: Security
language: JavaScript
comments_count: 5
repository_stars: 251891
---

Apply this rule to code paths that handle user-controlled data, parsed objects, or runtime environments:

1) Validate/whitelist inputs at multiple layers
- Prefer HTML constraints plus server/client normalization.
- Example (numeric-only field):
  ```js
  <input
    type="text"
    inputMode="numeric"
    pattern="[0-9]*"
    onChange={(e) => {
      const digitsOnly = e.target.value.replace(/\D/g, '');
      setValue(digitsOnly);
    }}
  />
  ```

2) Use safe property access when traversing parsed/untrusted objects
- When walking objects derived from external/protocol input, guard with `hasOwnProperty` (or an equivalent safe-iteration strategy like cloning onto a null-prototype object) so you don’t traverse unexpected prototype/injected properties.

3) Avoid leaking implementation details in production
- Don’t preserve constructor names/error metadata that can reveal internals.
- Use dev-only assertions/tests to verify rich diagnostics, but in `!__DEV__` return/emit sanitized errors.

4) Contain unsafe runtime mechanisms (e.g., `eval`) to the narrowest scope
- Only use when strictly required (often dev tooling).
- If using `eval`, don’t swallow failures silently—log the caught error details and ensure the check is located near where `eval` is actually used.
- Prefer non-`eval` alternatives when the environment supports them.

5) Encode/escape for the exact output context
- When generating headers/markup-like strings (e.g., Link headers), ensure escaping is correct for that specific syntax and newline/terminator constraints.

Adopting this checklist prevents injection, reduces prototype-traversal risk, and limits sensitive data exposure while still allowing necessary dev-time tooling.