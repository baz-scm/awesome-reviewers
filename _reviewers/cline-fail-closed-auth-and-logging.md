---
title: Fail-Closed Auth And Logging
description: 'Security standard: authentication/authorization and credential-handling
  code must fail closed and must not leak secrets.


  1) Auth callback state/nonce enforcement (fail-closed)'
repository: cline/CLINE
label: Security
language: TypeScript
comments_count: 11
repository_stars: 70839
---

Security standard: authentication/authorization and credential-handling code must fail closed and must not leak secrets.

1) Auth callback state/nonce enforcement (fail-closed)
- Treat state/nonce as a real anti-forgery control, not a best-effort prompt trigger.
- If `state` doesn’t match the expected value, do **not** proceed. Only proceed after an explicit, deliberate allow-list decision.
- Use a nonce that is per-auth-request (or validate against a short-lived bounded set). Do not reuse a long-lived “single nonce for the extension lifetime.”

Example pattern:
```ts
// Fail-closed: state mismatch must not store attacker-provided tokens.
if (authService.authNonce !== state) {
  const choice = await vscode.window.showWarningMessage(
    "Authentication response could not be verified. Store the token?",
    { modal: true },
    "Store",
  );
  if (choice !== "Store") return;
}
// Safe to continue only after verification.
if (token) authService.storeToken(token);
```

2) Production-safe logging: never log secrets
- In production, log only narrow metadata (e.g., error names/messages) and never serialize arbitrary strings/objects as extra log arguments.
- Redact URLs to `origin` at minimum; never include path/query/fragment where OAuth codes, tokens, or API keys may appear.
- Follow the rule: “call sites must not build secrets into error/log strings.” Prefer structured logging with redaction.

Example logging policy:
```ts
function redactUrlForLog(url: string): string {
  try {
    const u = new URL(url);
    if (u.origin === "null") return `${u.protocol}<redacted>`;
    return u.origin; // drop pathname/query/fragment
  } catch {
    return "<invalid url>";
  }
}

// In production logger: treat extra args as potentially secret; drop most.
```

3) Identity-safe boundaries when “loosening” security
- When credential state or ownership could be ambiguous (e.g., manual API-key save vs existing OAuth tokens, capability transfer across clients, sandbox write grants), gate changes strictly on verifiable conditions and avoid silent fallbacks.
- Prefer: “only clear/transfer when an actual security-relevant trigger exists,” otherwise keep the existing identity/boundary.

Adopting these rules prevents attacker-controlled auth bindings (fail-open) and prevents credential exfiltration through logs, telemetry, and error messages.