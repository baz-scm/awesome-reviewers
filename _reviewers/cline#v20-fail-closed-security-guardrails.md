---
title: Fail-Closed Security Guardrails
description: 'Security-critical decisions must be **fail-closed** (no silent fallbacks),
  and **secret-bearing data must never be logged verbatim**.


  Apply this standard in three places:'
repository: cline/cline#v20
label: Security
language: TypeScript
comments_count: 7
repository_stars: 70886
---

Security-critical decisions must be **fail-closed** (no silent fallbacks), and **secret-bearing data must never be logged verbatim**.

Apply this standard in three places:
1) **Auth / callback validation**
- If a verification check fails (e.g., OAuth `state` mismatch), only proceed on an explicit allow-list user action.
- Treat “dismissed”, “Esc”, or `undefined` as **cancel**, not as “continue”.
- Ensure any anti-forgery token/nonce is actually rotated per auth attempt (or otherwise time/usage-bounded), not a long-lived session constant.

Example (pattern):
```ts
if (authService.authNonce !== state) {
  const userChoice = await vscode.window.showWarningMessage(
    "The authentication response could not be verified. Store the token returned from this page?",
    { modal: true },
    "Store",
  );
  // undefined/dismiss => fail closed
  if (userChoice !== "Store") return;
}
```

2) **Capabilities / ownership routing**
- Never “transfer” or “pick the first registrant” when capability semantics could differ.
- If the intended owner disappears (disconnected/detached/cancelled-while-waiting), the request should **fail clearly** and be observable via structured reasons/telemetry.

3) **Logging / telemetry hygiene**
- Centralize URL redaction (e.g., reduce to `origin` / scheme) before logging.
- In production, logging should drop non-primitive values and avoid stringifying arbitrary error objects (including parse errors that may quote input).
- Avoid constructing error messages from secrets; treat “error message assembly” as part of the call-site attack surface.

This prevents the main classes of issues seen here: replay/fail-open auth callbacks, silent behavior changes from capability fallbacks, and accidental credential leakage via logs or error serialization.