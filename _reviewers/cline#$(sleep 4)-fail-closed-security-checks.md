---
title: Fail-closed security checks
description: 'Security-relevant decisions — auth/state validation, sandbox write boundaries,
  and security-affecting settings — must default to the denied/safe outcome and only
  proceed on an explicit, affirmative signal. Treat every ambiguous, error, or dismissed
  state as "deny", not "allow":'
repository: cline/cline#$(sleep 4)
label: Security
language: TypeScript
comments_count: 5
repository_stars: 70978
---

Security-relevant decisions — auth/state validation, sandbox write boundaries, and security-affecting settings — must default to the denied/safe outcome and only proceed on an explicit, affirmative signal. Treat every ambiguous, error, or dismissed state as "deny", not "allow":

- For user-confirmation gates guarding untrusted input (e.g. an OAuth callback whose `state` doesn't match the stored nonce), check for the one explicit approval value and treat everything else — including a dismissed dialog, which resolves to `undefined`, not `"Cancel"` — as rejection. Prefer a modal prompt so dismissal can't be mistaken for approval:
  ```ts
  if (authService.authNonce !== state) {
    const confirmed = await vscode.window.showWarningMessage(
      "This sign-in could not be verified. Continue only if you started it.",
      { modal: true },
      "Store",
    )
    if (confirmed !== "Store") return // dismiss, Esc, click-away all deny
  }
  ```
  Also, anti-forgery nonces must be freshly generated per auth request, not a single value reused for the life of the process — a stale, reusable nonce defeats the replay protection the check is meant to provide.

- For filesystem/sandbox boundaries (e.g. "only allow writes inside the project"), never grant write access to a directory without validating it first. Resolve real paths and reject the grant — loudly, with a clear error — when it resolves to a volume/filesystem root, the home directory, or an ancestor of it. A bare `cwd` can legitimately be `~` or a drive root, which would otherwise make the "sandbox" a no-op.

- For settings that gate a security feature, a failed or corrupt read must not be indistinguishable from "off was explicitly chosen." Fail closed, and when possible distinguish "file absent" (expected default) from "file exists but unreadable" (torn/corrupt write) so the unreadable case can be surfaced via a log or warning instead of silently losing protection.

When adding or reviewing any security gate, ask: what happens on the exception path, the cancel path, and the "value is absent" path? Each must resolve to the restrictive behavior by construction, not by the absence of a bug.