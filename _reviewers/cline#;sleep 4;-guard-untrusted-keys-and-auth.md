---
title: Guard untrusted keys and auth
description: 'Never let untrusted or dynamic input control a security-relevant decision
  without validation at the point of use. Two recurring patterns to guard against:'
repository: cline/cline#;sleep 4;
label: Security
language: TSX
comments_count: 2
repository_stars: 70976
---

Never let untrusted or dynamic input control a security-relevant decision without validation at the point of use. Two recurring patterns to guard against:

1. Unsafe dynamic property access (prototype pollution risk): when looking up a value in a plain object using a string derived from user/file input (e.g. file extension, file name, folder name), a plain `obj[key]` access can accidentally return inherited properties such as `constructor`, `__proto__`, or `toString` if the key happens to match one of them. Always verify the key is an own property before using the looked-up value, e.g.:
```ts
function lookup(table: Record<string, IconSpec>, key: string): IconSpec | undefined {
  return Object.hasOwn(table, key) ? table[key] : undefined;
}
```
Add regression tests for adversarial keys like `"constructor"`, `"__proto__"`, and `"toString"` to confirm they fall back to the default/neutral behavior instead of leaking prototype methods.

2. Authorization/eligibility checks must be re-validated at the moment of use, not inferred from a feature flag or stale cached state. If a UI action or command depends on a privileged resource (e.g. repo access, cloud connection), the backend operation that actually performs the privileged action must independently verify current authorization (and dirty/remote state) rather than trusting cached manifest data or client-side flags as proof of eligibility. Front-end gating to improve UX is fine, but it is not a substitute for server-side verification before the sensitive action executes.

Applying both principles prevents prototype-pollution-style data leaks and ensures that authorization decisions are never made on stale or spoofable client state.</description>
</invoke>
