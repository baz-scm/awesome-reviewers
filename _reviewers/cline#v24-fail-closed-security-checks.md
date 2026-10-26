---
title: Fail-closed security checks
description: For any security-sensitive flow (auth/callback validation, capability
  ownership/transfer, input-based trust decisions), default to denial and only proceed
  on an explicit allow-list condition. Separately, ensure logs never include credentials/secrets
  (especially OAuth tokens, URLs with query/userinfo, or error text that could embed
  sensitive values).
repository: cline/cline#v24
label: Security
language: TypeScript
comments_count: 6
repository_stars: 70891
---

For any security-sensitive flow (auth/callback validation, capability ownership/transfer, input-based trust decisions), default to denial and only proceed on an explicit allow-list condition. Separately, ensure logs never include credentials/secrets (especially OAuth tokens, URLs with query/userinfo, or error text that could embed sensitive values).

Apply this checklist:

1) Fail closed on validation/UI outcomes
- If a security check fails (e.g., auth `state` mismatch), proceed only when the user takes an explicit “Store/Allow” action.
- Never treat “dismissed notification / undefined” as approval.
- Prefer restoring the original hard boundary when it’s supposed to provide anti-forgery/replay protection (or otherwise explicitly document and redesign nonce lifetime).

Example pattern (auth state mismatch):
```ts
if (authService.authNonce !== state) {
  const userConfirmation = await vscode.window.showWarningMessage(
    `Authentication response could not be verified. Store the token returned from ${uri.path}?`,
    { modal: true },
    'Store'
  );
  if (userConfirmation !== 'Store') return; // deny by default
}
```

2) No implicit security capability takeover
- Do not “pick the first attached registrant” for security-relevant capabilities.
- If the original owner is gone, fail clearly (and emit telemetry) rather than silently changing behavior.

3) Secret-safe logging by default
- Redact URLs in logs to the minimum safe form (e.g., origin-only). Never log full paths/queries/fragments/userinfo that may contain OAuth codes/tokens.
- In production, narrow log serialization to non-sensitive primitives; treat error messages as untrusted input (avoid leaking raw error text that may include parsed secrets).

Rule of thumb: if code can store tokens, transfer security-relevant execution rights, or write sensitive data to logs, require explicit, allow-list-controlled conditions and default-deny behavior.