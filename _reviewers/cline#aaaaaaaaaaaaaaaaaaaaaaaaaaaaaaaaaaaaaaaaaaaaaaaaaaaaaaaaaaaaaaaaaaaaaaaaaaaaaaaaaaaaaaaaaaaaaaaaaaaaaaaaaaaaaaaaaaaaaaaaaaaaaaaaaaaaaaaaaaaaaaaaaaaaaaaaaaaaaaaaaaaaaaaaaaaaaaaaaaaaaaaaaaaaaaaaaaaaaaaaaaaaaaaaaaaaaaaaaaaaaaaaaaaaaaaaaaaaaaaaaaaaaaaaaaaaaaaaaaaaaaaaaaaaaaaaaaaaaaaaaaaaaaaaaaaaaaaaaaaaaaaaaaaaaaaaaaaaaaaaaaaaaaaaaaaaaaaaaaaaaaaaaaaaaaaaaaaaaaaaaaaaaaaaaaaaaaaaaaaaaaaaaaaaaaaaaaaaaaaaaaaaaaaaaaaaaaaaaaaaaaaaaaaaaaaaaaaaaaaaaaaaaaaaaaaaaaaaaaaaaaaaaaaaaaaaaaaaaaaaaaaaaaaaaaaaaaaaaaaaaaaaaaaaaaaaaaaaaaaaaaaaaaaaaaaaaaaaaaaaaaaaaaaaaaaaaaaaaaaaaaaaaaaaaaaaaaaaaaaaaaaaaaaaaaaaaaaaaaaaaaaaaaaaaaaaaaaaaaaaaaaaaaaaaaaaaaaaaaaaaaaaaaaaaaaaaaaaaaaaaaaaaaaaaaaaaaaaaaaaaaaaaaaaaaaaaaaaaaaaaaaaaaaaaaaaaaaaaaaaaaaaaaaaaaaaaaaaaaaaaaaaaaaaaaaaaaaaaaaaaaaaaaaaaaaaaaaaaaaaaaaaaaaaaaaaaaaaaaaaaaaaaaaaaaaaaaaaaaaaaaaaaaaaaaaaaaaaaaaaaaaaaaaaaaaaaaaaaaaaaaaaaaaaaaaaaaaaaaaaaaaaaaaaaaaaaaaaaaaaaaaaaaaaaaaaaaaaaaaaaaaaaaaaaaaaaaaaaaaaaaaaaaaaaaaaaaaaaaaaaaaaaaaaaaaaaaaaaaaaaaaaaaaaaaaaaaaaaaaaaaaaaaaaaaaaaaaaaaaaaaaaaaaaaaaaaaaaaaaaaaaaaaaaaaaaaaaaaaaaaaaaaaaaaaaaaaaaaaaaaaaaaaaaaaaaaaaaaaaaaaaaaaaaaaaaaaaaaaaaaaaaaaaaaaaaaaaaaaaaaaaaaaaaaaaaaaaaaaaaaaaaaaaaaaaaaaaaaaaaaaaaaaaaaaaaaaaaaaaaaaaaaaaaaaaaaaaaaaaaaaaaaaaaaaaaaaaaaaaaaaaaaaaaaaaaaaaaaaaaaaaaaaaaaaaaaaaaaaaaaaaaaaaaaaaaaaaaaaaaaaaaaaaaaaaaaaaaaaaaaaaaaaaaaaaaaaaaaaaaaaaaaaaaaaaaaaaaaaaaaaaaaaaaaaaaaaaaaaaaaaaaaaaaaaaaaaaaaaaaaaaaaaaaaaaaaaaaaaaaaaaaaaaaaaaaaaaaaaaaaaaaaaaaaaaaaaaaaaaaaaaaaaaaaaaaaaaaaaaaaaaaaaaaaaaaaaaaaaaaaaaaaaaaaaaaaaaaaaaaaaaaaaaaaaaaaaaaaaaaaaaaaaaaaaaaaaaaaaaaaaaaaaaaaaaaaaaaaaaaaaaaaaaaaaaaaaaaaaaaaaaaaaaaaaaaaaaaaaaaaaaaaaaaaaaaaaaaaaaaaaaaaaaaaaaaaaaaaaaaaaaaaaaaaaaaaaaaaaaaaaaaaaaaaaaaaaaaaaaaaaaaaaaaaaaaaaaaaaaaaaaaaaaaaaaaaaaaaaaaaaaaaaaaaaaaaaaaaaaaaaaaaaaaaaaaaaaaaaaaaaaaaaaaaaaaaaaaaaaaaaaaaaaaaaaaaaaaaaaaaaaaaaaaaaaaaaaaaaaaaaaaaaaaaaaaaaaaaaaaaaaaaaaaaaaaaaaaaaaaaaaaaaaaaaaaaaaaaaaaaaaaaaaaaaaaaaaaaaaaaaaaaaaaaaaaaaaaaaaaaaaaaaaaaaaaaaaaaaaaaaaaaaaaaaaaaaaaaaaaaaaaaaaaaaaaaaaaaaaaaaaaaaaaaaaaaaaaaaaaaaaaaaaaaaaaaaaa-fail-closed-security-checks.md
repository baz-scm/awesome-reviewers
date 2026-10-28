---
title: Fail-closed security checks
description: Any check that guards a security-sensitive action (auth/state validation,
  anti-forgery nonces, sandbox/protection toggles, cross-account authorization) must
  deny by default whenever the outcome is ambiguous, unknown, or not an explicit affirmative
  action — never fall through to the permissive path.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Security
language: TypeScript
comments_count: 4
repository_stars: 70976
---

Any check that guards a security-sensitive action (auth/state validation, anti-forgery nonces, sandbox/protection toggles, cross-account authorization) must deny by default whenever the outcome is ambiguous, unknown, or not an explicit affirmative action — never fall through to the permissive path.

Concretely:
- When asking the user to confirm a risky action, treat dismissal, Esc, or any response other than an explicit opt-in as a rejection. Prefer an allow-list check (`result !== "Store"`) over a deny-list check (`result === "Cancel"`), and use a modal prompt so there is no accidental default:
```ts
if (authService.authNonce !== state) {
    const confirmed = await vscode.window.showWarningMessage(
        "The authentication response could not be verified. Store the token returned?",
        { modal: true },
        "Store",
    )
    if (confirmed !== "Store") {
        return // dismiss, Cancel, or anything else denies by default
    }
}
```
- Anti-forgery tokens (CSRF/OAuth state nonces) must be freshly generated per request and validated as a genuine security boundary, not just used to decide whether to show a prompt. A single nonce generated once per process lifetime and never rotated provides no replay/forgery protection — rotate or bound acceptance to a short-lived set of recent nonces.
- When a setting or state that gates a protection (e.g., sandboxing, encryption, access control) cannot be read reliably (corrupt file, torn write, unknown state), do not silently fall back to "disabled" while reporting or assuming it is still "on". Either fail closed (keep protection enabled) or surface the degraded state explicitly (log/warn) so the gap is visible instead of silent.
- Re-validate authorization/ownership at the point of use for any multi-step or asynchronous privileged flow, so an approval or credential captured earlier cannot be replayed under a different account or context once circumstances have changed.

The common failure mode across these cases is designing the "unhappy path" (user dismissed, data unreadable, account/account scope changed) to default to the trusting behavior. Always make the secure/denied outcome the default, and require an explicit, verifiable signal to proceed.