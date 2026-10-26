---
title: Secure input and output
description: 'Apply security-hardening principles at trust boundaries and when encoding/decoding
  data:


  1) Constrain user-controlled inputs (client + handler)

  - Prefer HTML constraints (`pattern`, `inputMode`) and still normalize/validate
  in the change handler.'
repository: facebook/react#b1
label: Security
language: JavaScript
comments_count: 7
repository_stars: 251878
---

Apply security-hardening principles at trust boundaries and when encoding/decoding data:

1) Constrain user-controlled inputs (client + handler)
- Prefer HTML constraints (`pattern`, `inputMode`) and still normalize/validate in the change handler.
- Example pattern used for numeric-only:
  ```jsx
  <input
    type="text"
    inputMode="numeric"
    pattern="[0-9]*"
    onChange={e => {
      const digitsOnly = e.target.value.replace(/\D/g, '');
      // set state from digitsOnly
    }}
  />
  ```

2) Prevent production data leakage
- Don’t preserve/serialize developer-only details (e.g., error constructor identity) in prod error surfaces.
- If something is not serialized in prod, don’t implement prod deserialization for it (defense in depth).

3) Harden parsing/traversal against hostile object shapes
- When drilling into objects derived from untrusted data, use strict own-property checks (e.g., `hasOwnProperty.call(obj, key)`) before accessing children.
- This prevents traversing attacker-injected properties and gadget-like structures.

4) Preserve CSP correctness (nonce integrity)
- If the runtime uses CSP nonces (especially for streaming/inserted markup), require and propagate nonce values consistently.
- Avoid merging/combining chunks in ways that would produce markup with an incorrect or mismatched nonce.

5) Avoid `eval` when a safer construction exists
- If tests or instrumentation require dynamic behavior, prefer creating real instances/APIs directly (e.g., using a provided `window.MutationObserver`) rather than `eval`-ing code strings.