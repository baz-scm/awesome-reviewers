---
title: Fail-closed trust boundaries
description: Every security-sensitive check (file path containment, sandbox write
  grants, session/account scope, auth state validation, privileged command access)
  must validate against an explicit, fully-resolved boundary and must fail closed
  when that validation is ambiguous, incomplete, or bypassed.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Security
language: TypeScript
comments_count: 12
repository_stars: 70965
---

Every security-sensitive check (file path containment, sandbox write grants, session/account scope, auth state validation, privileged command access) must validate against an explicit, fully-resolved boundary and must fail closed when that validation is ambiguous, incomplete, or bypassed.

Concretely:
- Resolve paths to their real, symlink-resolved form before checking containment, and reject anything that escapes the intended root with a strict prefix/segment check (not a naive string match that a name like `..notes` or `draft*` could defeat).
- Never derive a sandbox or filesystem grant from an unvalidated value like a raw `cwd`; resolve it first and refuse (with a clear error) if the resolved path is a volume/filesystem root, the home directory, or an ancestor of it.
- Gate every privileged or data-exposing command on an explicit trust/ownership check at the point of use — don't assume a caller is trusted just because a sibling command on the same object is gated, or because an account/session "scope" was validated earlier in the flow; carry and re-check that scope across async boundaries so a stale approval can't apply after the account/session changed.
- Treat security token/state validation (nonce, CSRF state, auth callback state) as reject-by-default: an ambiguous, dismissed, or unhandled user response must never fall through to the "allow" branch. Use an explicit allow-list check (`result === "Approve"`) rather than an explicit deny-list check (`result !== "Cancel"`).
- When a security-relevant setting or piece of state can't be read reliably (torn write, corrupt file, missing permission), default to the protective/restrictive behavior and surface the ambiguity (log or user-visible warning) rather than silently falling back to the permissive state.

Example of the reject-by-default pattern for a confirmation gate:
```ts
if (authService.authNonce !== state) {
  const confirmation = await vscode.window.showWarningMessage(
    "This sign-in could not be verified. Continue only if you started it.",
    { modal: true },
    "Store",
  )
  if (confirmation !== "Store") {
    return // any dismissal, Escape, or unhandled response is a rejection
  }
}
```