---
title: Fail-closed security boundaries
description: Security-critical checks—authentication confirmations, sandbox resource
  grants, and path containment—must default to denying access and only proceed on
  an explicit, affirmative action, never on the absence of a negative one.
repository: cline/cline#`sleep 4`
label: Security
language: TypeScript
comments_count: 8
repository_stars: 70979
---

Security-critical checks—authentication confirmations, sandbox resource grants, and path containment—must default to denying access and only proceed on an explicit, affirmative action, never on the absence of a negative one.

- **Auth/consent prompts**: Treat dismissal, timeout, or any response other than the exact expected affirmative action as a decline. Never structure a check as `if (result === "Cancel") deny` when the underlying API can resolve to `undefined`; invert it to `if (result !== "Confirm") deny`, and prefer modal prompts so there is no accidental default path. For example:
```ts
if (authService.authNonce !== state) {
  const confirmation = await vscode.window.showWarningMessage(
    "This sign-in could not be verified. Continue only if you started it.",
    { modal: true },
    "Store",
  )
  if (confirmation !== "Store") return // anything else, including dismissal, denies
}
```
Also ensure the underlying token (e.g., a CSRF nonce) is actually rotated/validated and not just used to gate a UI prompt—downgrading a security check to a confirmation dialog without preserving the original anti-forgery guarantee reintroduces the vulnerability it replaced.

- **Sandbox/permission grants**: Never grant read-write or elevated access to a directory without first resolving it to a real, canonical path and checking it isn't a volume root, filesystem root, home directory, or ancestor thereof. A session or request-supplied `cwd`/root is not inherently trustworthy just because "there's nothing more trusted to source it from"—if the boundary matters, gate the underlying transport/connection itself (e.g., require a trusted/authenticated connection) rather than relying solely on a path coherence check.

- **Path containment**: When confining file access to a root (project explorers, rule file writers, etc.), resolve symlinks via `realpath` before validating containment, and match traversal segments precisely (e.g., only a literal `..` or a `../`/`..\\` prefix, not any substring like `..notes`). If following symlinks outside the root is an intentional, documented product decision, state that explicitly in code comments rather than leaving the containment check looking like a complete boundary.

Apply this "deny unless explicitly allowed" posture consistently whenever code decides whether to trust user input, a client connection, or a filesystem path as a security boundary.