---
title: Backend Enforcement, UI Validation
description: Treat the frontend as an *UX layer*, not an authorization or confidentiality
  enforcement boundary. Any access control (licensing, revoke/re-auth, hidden-content
  guarantees, RBAC) must be enforced by the backend/data layer; the UI may be redundant
  or fail-open without granting access. Separately, whenever the UI must render untrusted
  values into...
repository: maximhq/bifrost
label: Security
language: TSX
comments_count: 5
repository_stars: 6862
---

Treat the frontend as an *UX layer*, not an authorization or confidentiality enforcement boundary. Any access control (licensing, revoke/re-auth, hidden-content guarantees, RBAC) must be enforced by the backend/data layer; the UI may be redundant or fail-open without granting access. Separately, whenever the UI must render untrusted values into security-sensitive contexts (e.g., hyperlinks), validate/allow-list before using them.

Apply this as a standard:
- **Authorization/confidentiality:** must be enforced in server middleware, RBAC/DAC checks, and/or storage/query logic. UI conditions are allowed for user guidance but never as the source of truth.
- **Destructive or identity-sensitive actions:** ensure the backend’s scope/authorization is correct; don’t rely on hiding the button or owner-gating in React.
- **Defense-in-depth:** it’s acceptable to repeat RBAC checks in nested routes (consistent with app style), as long as backend enforcement remains the ultimate gate.
- **Untrusted rendering:** before using any user-/server-provided string in `href` (or other executable/sensitive contexts), apply an allow-list policy and fall back to safe rendering (e.g., plain text).

Example pattern (safe URL rendering):
```ts
const uri = deviceState.verificationUri;
const safe = /^https:\/\/([a-z0-9-]+\.)*github\.com(\/|$)/i.test(uri);

return safe ? (
  <a href={uri} target="_blank" rel="noopener noreferrer">Open link</a>
) : (
  <code>{uri}</code>
);
```

If you’re tempted to add a UI-only `if (shouldHide) return null`, confirm the backend/storage already prevents the underlying data/action; otherwise, move or add the enforcement where it can’t be bypassed.