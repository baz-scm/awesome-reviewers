---
title: Fail-closed Trust Boundaries
description: Security decisions must be explicit and default to refusal when verification
  fails, instead of relying on fallbacks or permissive prompts. This includes capability
  routing, auth callbacks, sandbox filesystem grants, and any write/modify scope.
repository: cline/cline#v25
label: Security
language: TypeScript
comments_count: 9
repository_stars: 70891
---

Security decisions must be explicit and default to refusal when verification fails, instead of relying on fallbacks or permissive prompts. This includes capability routing, auth callbacks, sandbox filesystem grants, and any write/modify scope.

Apply these rules:
- **Auth callbacks:** If `state` (or equivalent CSRF/anti-forgery proof) doesn’t match, proceed only on an explicit allow-list user action (e.g., “Store”), otherwise return without storing tokens. Dismiss/close/undefined results must not continue.
- **Routing/ownership:** Never silently transfer or “pick the first registrant” when ownership/policy compatibility isn’t proven; if safe takeover isn’t explicitly defined, fail clearly and emit telemetry.
- **Sandbox/filesystem writes:** Always **resolve** (e.g., `realpath`) and validate that read/write grants are inside the intended working root. Fail closed if the computed writable path is or is an ancestor of filesystem roots, home directories, or volume roots.
- **Logging/errors:** Treat any free-form strings (URLs, error messages, JSON-serialized objects) as potentially secret-bearing. Redact or reduce URLs to origin, and in production narrow logged data to error messages without stacks/secrets.

Example (fail-closed auth mismatch):
```ts
if (authService.authNonce !== state) {
  const ok = await vscode.window.showWarningMessage(
    `Unverified authentication response. Store token from ${uri.path}?`,
    { modal: true },
    "Store"
  );
  if (ok !== "Store") return; // dismissed/close => refuse
}
// only now is token storage allowed
```