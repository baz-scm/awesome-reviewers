---
title: Fail-Closed Security Handling
description: 'Security-critical flows must fail closed: when verification or containment
  checks don’t pass, do not proceed with storing/using sensitive material. Avoid “dismissed
  prompt == allow”, and ensure that logs/telemetry and filesystem/sandbox permissions
  do not leak or over-grant.'
repository: cline/cline#v12
label: Security
language: TypeScript
comments_count: 9
repository_stars: 70872
---

Security-critical flows must fail closed: when verification or containment checks don’t pass, do not proceed with storing/using sensitive material. Avoid “dismissed prompt == allow”, and ensure that logs/telemetry and filesystem/sandbox permissions do not leak or over-grant.

**1) Auth state/verification: deny by default**
- If CSRF/state/handshake verification fails, only continue on an explicit, positively chosen allow action.
- Treat any dismissed/closed/undefined prompt result as **cancel**.

```ts
// Fail-closed pattern
if (authService.authNonce !== state) {
  const choice = await vscode.window.showWarningMessage(
    "Authentication could not be verified. Store the token?",
    { modal: true },
    "Store",
    "Cancel",
  )
  if (choice !== "Store") return; // dismiss/cancel => do not store
}

// Only now is it safe to persist tokens
if (token) await authService.storeToken(token);
```

**2) Secrets in logs: redact + restrict**
- Redact sensitive URLs (OAuth codes/tokens/userinfo/paths) before logging; prefer `origin` only.
- In production, restrict structured logging to safe primitives and error messages; avoid logging arbitrary strings/objects as extra args.

```ts
export function redactUrlForLog(url: string): string {
  try {
    const u = new URL(url)
    return u.origin === "null" ? `${u.protocol}<redacted>` : u.origin
  } catch {
    return "<invalid url>"
  }
}
```

**3) Containment for untrusted inputs (paths/sandbox): explicit allow-lists**
- For filesystem operations, enforce that paths resolve inside allowed roots (resolve symlinks/real paths) and deny traversal escapes.
- For sandbox write permissions, fail closed if the requested writable grant would include home, filesystem roots, or ancestor volumes.

If a check is intended to be security-relevant, the code should be written so that the default outcome is **no sensitive state change** and **no secret leakage** unless all verification/containment conditions pass.