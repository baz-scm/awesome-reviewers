---
title: Defend Security-Sensitive Rendering
description: 'Apply defense-in-depth whenever code touches user-controlled data or
  generates security-relevant output (inputs, errors, streamed rendering, CSP-protected
  tags):'
repository: facebook/react#b14
label: Security
language: JavaScript
comments_count: 5
repository_stars: 251893
---

Apply defense-in-depth whenever code touches user-controlled data or generates security-relevant output (inputs, errors, streamed rendering, CSP-protected tags):

1) Validate/normalize at the UI boundary and enforce in the handler
- Use both declarative constraints and runtime normalization so the value cannot drift.
- Example (digit-only field):
  ```jsx
  <input
    type="text"
    inputMode="numeric"
    pattern="[0-9]*"
    onChange={e => {
      const digitsOnly = e.target.value.replace(/\D+/g, '');
      // setState(digitsOnly)
    }}
  />
  ```

2) Avoid information disclosure in production
- Keep rich error/diagnostic details (e.g., constructor names) in dev, but in production avoid preserving details that can reveal implementation internals.
- Example pattern:
  ```js
  const safeName = __DEV__ ? originalError.name : 'Error';
  ```

3) Traverse objects safely (no prototype/foreign property drilling)
- When walking parsed or externally influenced structures, require own-property checks before accessing fields.
- Example:
  ```js
  const key = path[i];
  if (typeof value === 'object' && value !== null && Object.prototype.hasOwnProperty.call(value, key)) {
    value = value[key];
  }
  ```

4) Preserve CSP nonce semantics; don’t assume nonce compatibility
- Ensure nonce values used for generated tags are correctly propagated, including pre-initialization flows.
- Don’t merge or reuse security-sensitive rendered content across different nonces; treat “nonce differs” as a hard boundary.
- Also ensure risky mechanisms (like `eval`) are properly located and gated to dev/controlled code paths to minimize exposure.

These rules reduce input-driven abuse, gadget/prototype traversal risks, and security header mismatches, while limiting production leakage of internal details.