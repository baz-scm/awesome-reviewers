---
title: Fail-closed security boundaries
description: Security-critical checks (authentication state validation, sandbox/permission
  gates, path containment) must default to the safe, denied state whenever the outcome
  is ambiguous, errored, or unconfirmed — never fail open. Prefer explicit allow-lists
  over negative conditions, since any unhandled branch (a dismissed dialog, an unreadable
  settings file, an...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Security
language: TypeScript
comments_count: 6
repository_stars: 70968
---

Security-critical checks (authentication state validation, sandbox/permission gates, path containment) must default to the safe, denied state whenever the outcome is ambiguous, errored, or unconfirmed — never fail open. Prefer explicit allow-lists over negative conditions, since any unhandled branch (a dismissed dialog, an unreadable settings file, an unvalidated path) then safely denies rather than silently proceeding.

Concretely:
- When confirming a risky action via a user prompt, only an explicit "allow" response should proceed; treat dismissal, Escape, or any other result as "deny." For example, prefer:
```ts
if (authService.authNonce !== state) {
  const confirmed = await vscode.window.showWarningMessage(
    "This sign-in could not be verified. Continue only if you started it.",
    { modal: true },
    "Store",
  )
  if (confirmed !== "Store") return // anything other than the explicit allow denies
}
```
rather than checking for the one disallow value (`=== "Cancel"`), which silently allows on any other outcome.
- When a security-relevant setting or state cannot be read reliably (e.g. a torn/corrupt settings file), do not silently fall back to the less restrictive default. Distinguish "not configured" from "failed to read," and prefer keeping the stricter last-known value or surfacing the failure, rather than defaulting to unsandboxed/unprotected behavior without telling the user.
- When establishing a filesystem or process sandbox boundary, explicitly validate that granted read-write roots are not a volume root, the home directory, or an ancestor of it — don't assume a boundary is safe just because it was constructed from a relative path. Resolve real paths before trusting them, and fail with a clear error instead of silently granting broader access than intended.
- Anti-forgery/state tokens (e.g. OAuth nonce/CSRF state) must be regenerated per request/session rather than fixed for the process lifetime, and must be strictly enforced, not merely used to decide whether to show a confirmation.

Apply this standard any time a change touches permission gates, sandbox boundaries, token/state validation, or settings that control whether an action is restricted — the safe path must be the default, and only an unambiguous, explicit signal should relax it.