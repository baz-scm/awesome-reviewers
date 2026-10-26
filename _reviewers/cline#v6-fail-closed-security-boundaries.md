---
title: Fail-Closed Security Boundaries
description: 'Always enforce security checks in a fail-closed way, and treat any “stringification/logging/output”
  as potentially secret-bearing.


  Apply these rules:'
repository: cline/cline#v6
label: Security
language: TypeScript
comments_count: 10
repository_stars: 70864
---

Always enforce security checks in a fail-closed way, and treat any “stringification/logging/output” as potentially secret-bearing.

Apply these rules:
1) **Auth/CSRF/state validation must be allow-list based**
- If verification fails, do not proceed based on “dismissed prompt” behavior.
- Use an explicit modal confirmation whose only allowed response is the deliberate action; anything else cancels.

```ts
// Fail-closed example: state mismatch
if (authService.authNonce !== state) {
  const choice = await vscode.window.showWarningMessage(
    `Could not verify auth response. Store the token returned from ${uri.path}?`,
    { modal: true },
    "Store",
  );
  if (choice !== "Store") return; // dismiss/esc/close => cancel
}
// proceed only when verified or explicitly allowed
```

2) **Never leak secrets via logs/errors**
- In production, log only safe primitives (e.g., message + error classification) and redact anything URL/credential-like.
- Reduce logged URLs to **origin** (scheme+host) and omit query/paths that may contain codes/tokens/keys.

```ts
export function redactUrlForLog(url: string): string {
  try {
    const u = new URL(url);
    if (u.origin === "null") return `${u.protocol}<redacted>`;
    return u.origin; // drop pathname/query/fragment
  } catch {
    return "<invalid url>";
  }
}
```

3) **Containment and ownership must be explicit (no silent fallbacks)**
- When selecting handlers/owners (capabilities, sessions, sandboxes), do not silently pick “the first attached registrant/next best” if the takeover contract isn’t explicitly compatible.
- For file/sandbox write permissions, ensure the writable root is not the filesystem root, home directory, or an ancestor/volume; compute and validate real paths.

4) **Path handling: symlinks and allowed roots**
- Resolve/validate request paths against allowed roots (including symlink escape checks when security boundary matters) and only read/write allowed file types.

These practices prevent: CSRF/token storage regressions, secret exfiltration through logs, and security boundary violations caused by permissive fallback logic or unsafe writable grants.