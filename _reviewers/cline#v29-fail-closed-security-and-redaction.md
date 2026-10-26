---
title: Fail-Closed Security and Redaction
description: 'Security checks must default to safe failure (no “dismissed/unknown”
  pass) and any secret-bearing data must be handled as untrusted: validate boundaries/ownership
  strictly before granting access, and redact anything that could contain credentials/tokens.'
repository: cline/cline#v29
label: Security
language: TypeScript
comments_count: 7
repository_stars: 70893
---

Security checks must default to safe failure (no “dismissed/unknown” pass) and any secret-bearing data must be handled as untrusted: validate boundaries/ownership strictly before granting access, and redact anything that could contain credentials/tokens.

Apply these rules:
1) Auth/callback/state guards: never proceed unless the check passes OR the user explicitly confirms an allow-list action.
2) Capability/ownership routing: disallow silent takeover fallbacks; if the intended owner is gone, fail with a clear error.
3) Filesystem/sandbox boundaries: compute real/normalized paths and deny write grants to dangerous roots/ancestors; if containment can’t be proven, deny.
4) Logging: do not log URLs/requests/errors that may contain OAuth codes, tokens, userinfo, or API keys; in production, only log safe primitives and error messages (not stacks/serialized objects with secrets).

Example (fail-closed auth callback):
```ts
if (authService.authNonce !== state) {
  const choice = await vscode.window.showWarningMessage(
    `The authentication response could not be verified. Store the token returned from ${uri.path}?`,
    { modal: true },
    "Store",
  );
  if (choice !== "Store") return; // fail closed: never store on dismiss/escape
}
```

Example (secret-safe URL logging):
```ts
export function redactUrlForLog(raw: string): string {
  try {
    const u = new URL(raw);
    return u.origin === "null" ? `${u.protocol}<redacted>` : u.origin;
  } catch {
    return "<invalid url>";
  }
}
```

If a change would require a “fallback” to keep going for safety/correctness, treat that as a security smell—make the fallback explicit and gated, or fail clearly.