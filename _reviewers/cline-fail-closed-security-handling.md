---
title: Fail-Closed Security Handling
description: 'Apply a single principle across auth, credentials, routing, sandboxing,
  and logging: **security must default to deny and must never proceed on ambiguous/dismissed
  outcomes; state and boundaries must be explicit and consistent.**'
repository: Cline/Cline
label: Security
language: TypeScript
comments_count: 13
repository_stars: 70840
---

Apply a single principle across auth, credentials, routing, sandboxing, and logging: **security must default to deny and must never proceed on ambiguous/dismissed outcomes; state and boundaries must be explicit and consistent.**

**Rules to standardize**
1) **Auth callbacks must be fail-closed**
- If verification (e.g., `state`) fails, only continue on an explicit allow action; dismissal (Esc/close/outside click) must not be treated as approval.
- Prefer `modal: true` (or an equivalent) and an allow-list check.

```ts
if (authService.authNonce !== state) {
  const choice = await vscode.window.showWarningMessage(
    `Could not verify auth response. Store token from ${uri.path}?`,
    { modal: true },
    "Store"
  );
  if (choice !== "Store") return; // fail closed
}
```

2) **Manual credential replacement must be deterministic**
- If the UX says “pasted API key replaces OAuth/browser sign-in”, ensure stale OAuth artifacts can’t silently win.
- Clear (or gate clearing of) superseded fields only when a real OAuth token is present, and handle identity updates consistently (then refetch if needed).
- Ensure probes and API clients use the same auth format (e.g., Bearer token).

3) **Security boundaries must be explicit and never widen**
- For sandboxes: never grant write access to unsafe paths derived from user-controlled or overly broad `cwd` (e.g., whole home directory, volume root, or ancestors). Resolve real paths and fail closed if the grant would be a root/volume/ancestor.
- For capability routing: do not silently “take over” based solely on a name match; require an explicit compatible takeover path, otherwise fail.

4) **Secrets must not leak to logs**
- Treat error messages and log arguments as untrusted: in production, only log safe primitives (numbers/booleans) and redact/strip credential-bearing URLs and query/path secrets.
- Ensure URL logging is reduced to a safe form (e.g., origin/limited parts) and unparseable inputs are not echoed.

**Adoption checklist**
- Any place that makes an auth/security decision: confirm the default path is deny.
- Any prompt on verification failure: ensure dismissed/undefined cannot proceed.
- Any credential persistence update: ensure “intended source wins” and superseded tokens/identity are handled intentionally.
- Any sandbox/capability routing logic: confirm it cannot select a broader permission/routing target by accident.
- Any logging: confirm no URLs/tokens/stack traces or error-message-built strings can include secrets in production.