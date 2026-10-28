---
title: Validate untrusted state at use
description: Never treat cached, inferred, or externally-controlled state as authoritative
  for a security decision — validate it at the exact point where it matters.
repository: cline/cline#`sleep 4`
label: Security
language: TSX
comments_count: 2
repository_stars: 70979
---

Never treat cached, inferred, or externally-controlled state as authoritative for a security decision — validate it at the exact point where it matters.

- Authorization/eligibility: don't gate privileged actions solely on feature flags or data cached earlier in the session (e.g., a workspace manifest's git URL recorded at session start). Re-check the actual authorization and resource state (e.g., live GitHub connection, repo access, dirty state, remote reachability) immediately before performing the privileged action.
- Untrusted keys in object lookups: when indexing a plain object with a string that can be influenced by user input or file/path data, guard against prototype-pollution-style lookups. Use `Object.hasOwn(obj, key)` (or a `Map`) before accessing the value, so keys like `constructor`, `__proto__`, or `toString` fall through to a safe default instead of returning an inherited prototype property.

```ts
// Unsafe: returns Object.prototype.constructor instead of undefined
const spec = BY_NAME[name];

// Safe
const spec = Object.hasOwn(BY_NAME, name) ? BY_NAME[name] : undefined;
```

Apply this pattern consistently: validate live state for anything authorization-related, and validate ownership for any dictionary-style lookup keyed by untrusted strings.