---
title: Fail Closed And Redact
description: 'Security-critical operations must default to *deny on ambiguity* and
  *avoid leaking secrets*.


  Apply two rules:

  1) Fail closed on security decisions: if identity/ownership/state can’t be verified
  (or the user doesn’t explicitly confirm), abort and do not store/act on sensitive
  results.'
repository: cline/cline#v19
label: Security
language: TypeScript
comments_count: 9
repository_stars: 70885
---

Security-critical operations must default to *deny on ambiguity* and *avoid leaking secrets*.

Apply two rules:
1) Fail closed on security decisions: if identity/ownership/state can’t be verified (or the user doesn’t explicitly confirm), abort and do not store/act on sensitive results.
2) Never emit secrets in logs/errors: in production, only log safe primitives; when logging URLs or error text that may embed credentials/tokens, redact to a non-sensitive form (e.g., origin only) and don’t echo full inputs.

Example (state mismatch must not be fail-open):
```ts
if (authService.authNonce !== state) {
  const userChoice = await vscode.window.showWarningMessage(
    `The authentication response could not be verified. Continue?`,
    { modal: true },
    "Store",
  );
  // Dismiss/ESC/close must cancel (fail closed)
  if (userChoice !== "Store") return;
}
// Only proceed when state is verified or the user explicitly chose to continue.
```

Example (URL redaction for logs):
```ts
export function redactUrlForLog(url: string): string {
  try {
    const u = new URL(url);
    if (u.origin === "null") return `${u.protocol}<redacted>`;
    return u.origin; // drop path/query/fragment that may contain secrets
  } catch {
    return "<invalid url>";
  }
}

Logger.info(`Opening server ${redactUrlForLog(serverUrl)}`);
```

Practical checklist:
- Any check that guards auth/CSRF/ownership must be deny-by-default.
- Treat “undefined”, dismissals, and timeouts as *not approved* unless the code explicitly allows them.
- In production logging, do not pass raw errors/objects/strings that may contain credentials, tokens, full URLs, or file contents; redact or restrict first.