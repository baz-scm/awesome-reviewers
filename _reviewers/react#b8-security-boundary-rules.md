---
title: Security Boundary Rules
description: 'When handling user/remote data or security-sensitive metadata, apply
  strict validation, safe traversal, and least-information principles.


  - Validate/whitelist at the boundary: constrain form inputs so the stored value
  can only be the expected characters.'
repository: facebook/react#b8
label: Security
language: JavaScript
comments_count: 6
repository_stars: 251889
---

When handling user/remote data or security-sensitive metadata, apply strict validation, safe traversal, and least-information principles.

- Validate/whitelist at the boundary: constrain form inputs so the stored value can only be the expected characters.
  ```js
  <input
    type="text"
    inputMode="numeric"
    pattern="[0-9]*"
    aria-label="Result index"
    value={value}
    onChange={e => {
      const digitsOnly = e.target.value.replace(/\D/g, '');
      setValue(digitsOnly);
    }}
  />
  ```

- Guard object traversal and deserialization paths: never drill into properties without confirming the property is owned by the object you expect.
  - Example rule: before `obj[prop]`, require `hasOwnProperty.call(obj, prop)` (or equivalent).

- Minimize prod data exposure: gate serialization/deserialization of error details (names/causes/implementation data) to dev-only when that data isn’t required.

- Treat CSP nonces as security-critical and non-mergeable: ensure `nonce` is consistently applied to the generated `<style>`/`<script>` content, and don’t merge/aggregate resources that could carry different nonces. Keep requiring author-provided nonces when React is emitting security-relevant tags.

Together, these practices reduce injection/gadget surfaces, prevent unintended information leaks, and maintain CSP correctness.