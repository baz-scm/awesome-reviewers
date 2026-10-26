---
title: Fail-closed secrets safe
description: 'Adopt one standard: when handling auth/capabilities, filesystem/tool
  boundaries, and logging, default to **fail-closed** and **never leak secrets**.


  1) Auth/capability boundaries must not fail open'
repository: cline/cline#v21
label: Security
language: TypeScript
comments_count: 14
repository_stars: 70886
---

Adopt one standard: when handling auth/capabilities, filesystem/tool boundaries, and logging, default to **fail-closed** and **never leak secrets**.

1) Auth/capability boundaries must not fail open
- If verification is mismatched/unknown, only proceed on an explicit allow-list action; treat dismissal/`undefined` as **cancel**.

```ts
if (authService.authNonce !== state) {
  const choice = await vscode.window.showWarningMessage(
    `Store the token returned from ${uri.path}?`,
    { modal: true },
    "Store",
  )
  if (choice !== "Store") return; // dismiss/esc/close => cancel
}
```
- Remove implicit fallbacks/ownership transfers that can silently change runtime behavior; fail clearly and track disconnect/detach/cancel.

2) Contain filesystem/tool permissions
- If “write access in project directory” is derived from `cwd`, resolve **real paths** and fail closed when the grant would include a volume/filesystem root or ancestors like the user home.
- Validate request paths with root containment (symlink behavior must be explicit and tested), and use literal path operations for git/source-control actions.

3) Secret-safe logging/telemetry
- In production, do not stringify/log arbitrary extra args (strings/objects/errors often carry tokens, file contents, URLs).
- Redact URLs before logging—keep only origin/scheme; never include query/path/userinfo.

```ts
export function redactUrlForLog(url: string): string {
  try {
    const u = new URL(url)
    return u.origin === "null" ? `${u.protocol}<redacted>` : u.origin
  } catch {
    return "<invalid url>"
  }
}

Logger.info("Opening browser:", redactUrlForLog(inputUrl))
```

Checklist: (a) can execution proceed on uncertain verification? (b) can user-controlled paths/`cwd` expand write boundaries or bypass containment? (c) could logs include secrets (URL query/path/userinfo, tokens, file contents)? If any answer is “yes/unknown”, change to fail-closed and redact at the source (or via a centralized safe logger).