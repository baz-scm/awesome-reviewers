---
title: Fail-closed Security Boundaries
description: 'Security-sensitive flows must be *fail-closed*: once identity/state/ownership
  can’t be verified, do not proceed, do not silently transfer, and do not expand privileges.'
repository: CLINE/CLINE
label: Security
language: TypeScript
comments_count: 8
repository_stars: 70837
---

Security-sensitive flows must be *fail-closed*: once identity/state/ownership can’t be verified, do not proceed, do not silently transfer, and do not expand privileges.

Apply these rules:
1) **Auth callbacks and state checks must be un-bypassable**
   - If a state/nonce mismatch occurs, only continue on an explicit allow-list user action (e.g. exact button label), and treat dismissal/Esc/close as **Cancel**.
   - Do not make nonces session-lifetime constants; generate per request (or short-lived bounded set) so replay is not viable.

   Example pattern:
   ```ts
   if (authService.authNonce !== state) {
     const choice = await vscode.window.showWarningMessage(
       "Auth response could not be verified. Continue?",
       { modal: true },
       "Store"
     );
     if (choice !== "Store") return; // dismiss == cancel
   }
   ```

2) **Security boundaries (capabilities, routing, sandboxes) must be explicit and constrained**
   - Never pick the “first attached” client/tool as a fallback for capability ownership; require an explicit compatible takeover contract or fail with a clear message.
   - For sandbox write permissions, validate resolved (real) paths and ensure read-write grants do **not** become writable volumes/roots/home or ancestors-of-home. If you can’t safely determine containment, deny the protected action.

3) **Secrets hygiene: production logging/output must not leak credentials**
   - Redact URLs down to origin at call sites that may include OAuth codes/tokens/userinfo; in production, only log narrow types (e.g. error message + numbers/booleans) and avoid serializing arbitrary strings/objects/errors that may contain credentials.
   - Treat “sensitive file” protections as security controls: cover common secret locations and keep regression tests for newly discovered secret patterns.

These practices prevent the most common security regressions shown in the discussions: fail-open auth paths, silent capability retargeting, overly-broad sandbox write grants, and credential leakage through logs.