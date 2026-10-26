---
title: Fail-Closed Auth and Secrets
description: 'Enforce a security baseline in authentication flows and diagnostics:


  1) **Auth callbacks must fail closed**

  - Treat `state`/nonce mismatches as unverified.'
repository: cline/cline#v1
label: Security
language: TypeScript
comments_count: 8
repository_stars: 70862
---

Enforce a security baseline in authentication flows and diagnostics:

1) **Auth callbacks must fail closed**
- Treat `state`/nonce mismatches as unverified.
- If the user is prompted, proceed **only** when the return value is an explicit, allow-listed action (e.g., the exact button label).
- Dismiss/escape/close (`undefined`) must **cancel**—never continue storing tokens.

```ts
// FAIL CLOSED: dismiss or any non-"Store" result cancels.
if (authService.authNonce !== state) {
  const result = await vscode.window.showWarningMessage(
    `Could not verify the auth response. Store token returned from ${uri.path}?`,
    { modal: true },
    "Store"
  );
  if (result !== "Store") return;
}
// Only here: persist token
if (token) await authService.storeToken(token);
```

2) **Never leak secrets in logs**
- Redact or drop sensitive URL components (query, fragment, userinfo, paths that may contain keys/tokens). Prefer a helper like `redactUrlForLog()` that reduces to `origin`/`scheme`.
- In production, restrict logger output to safe primitives (booleans/numbers) and **error names/messages only**—do not serialize full error objects/strings that may contain credential-bearing URLs.

3) **Keep filesystem/sandbox boundaries fail-closed**
- For project explorer/sandbox write grants, ensure the effective “write root” cannot accidentally become the user’s home directory, a filesystem root, or an ancestor that expands the boundary.
- When symlinks are allowed for user experience, document the intent and ensure the check still preserves the intended boundary.

Applying these consistently prevents: token/session binding regressions, credential exfiltration via logs, and overly-broad write permissions.