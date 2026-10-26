---
title: Fail-closed auth state
description: Security-sensitive flows must not “fail open”. If the authentication
  response cannot be verified (e.g., `state`/nonce mismatch), treat that as a hard
  failure by default—even if you show a UI prompt.
repository: cline/cline#v17
label: Security
language: TypeScript
comments_count: 5
repository_stars: 70883
---

Security-sensitive flows must not “fail open”. If the authentication response cannot be verified (e.g., `state`/nonce mismatch), treat that as a hard failure by default—even if you show a UI prompt.

Apply these rules:
1) **Dismissing/closing a prompt must deny.** Only continue on an explicit allow choice (exact string/button), never on `undefined`.
2) **Use state/nonce for real anti-forgery/replay.** If `state` is not rotated/used per request (or is bounded only by extension lifetime), don’t rely on it as a CSRF boundary.
3) **Don’t leak auth details in logs.** When reporting auth errors/callback URLs, redact to origin/path-only (or invalidate entirely), and in production restrict log extra-args to non-secret primitives.

Example pattern (TypeScript/VS Code-style):
```ts
if (authService.authNonce !== state) {
  const userChoice = await vscode.window.showWarningMessage(
    `Unverified authentication response from ${uri.path}`,
    { modal: true },
    "Store"
  );
  if (userChoice !== "Store") {
    return; // deny on dismiss/close/escape
  }
}

// When logging, never include full URLs/callback params
Logger.info("Auth callback received", redactUrlForLog(uri.toString()));
```

(Complement with URL redaction and production-safe logging utilities so auth failures don’t end up in bug reports with tokens/codes.)