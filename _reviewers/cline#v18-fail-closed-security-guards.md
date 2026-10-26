---
title: Fail-closed Security Guards
description: 'Security-sensitive flows must be *allowlist + default-deny* and must
  never “fail open” when verification fails.


  Apply this standard:

  - **Verification failure ⇒ stop.** If anti-forgery state / ownership / capability
  takeover compatibility checks don’t pass, return an error (or explicit cancel) and
  do not continue.'
repository: cline/cline#v18
label: Security
language: TypeScript
comments_count: 6
repository_stars: 70884
---

Security-sensitive flows must be *allowlist + default-deny* and must never “fail open” when verification fails.

Apply this standard:
- **Verification failure ⇒ stop.** If anti-forgery state / ownership / capability takeover compatibility checks don’t pass, return an error (or explicit cancel) and do not continue.
- **User prompts must be explicit allowlists.** Treat *dismiss/close/undefined* as **deny**, not as permission.
- **Authorization must be consistent.** Capabilities, sessions, and privileged operations must be gated on the correct owner/registrant; avoid implicit fallbacks like “pick the first attached registrant”.
- **Don’t leak secrets while enforcing.** When logging auth/security decisions, use structured-safe logging and URL redaction (never echo full URLs/queries/tokens).

Example (fixing a fail-open state mismatch):
```ts
// Default-deny on verification mismatch.
if (authService.authNonce !== state) {
  const choice = await vscode.window.showWarningMessage(
    `Could not verify auth response from ${uri.path}. Store token?`,
    { modal: true },
    "Store",
  );
  if (choice !== "Store") return; // dismissal/esc/undefined => deny
}
// proceed only when verification passed or user explicitly allowed
```

Rule of thumb: if the code contains “if (x) proceed” around security checks, ensure `x` is *strictly true only for verified/authorized conditions*; everything else is denial.