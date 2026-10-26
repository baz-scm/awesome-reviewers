---
title: Fail-Closed Security Boundaries
description: 'Treat any ownership transfer, auth verification, and filesystem/tool
  permission as a security boundary: validate the effective target, and fail closed
  by default.'
repository: cline/cline#x
label: Security
language: TypeScript
comments_count: 11
repository_stars: 70861
---

Treat any ownership transfer, auth verification, and filesystem/tool permission as a security boundary: validate the effective target, and fail closed by default.

Practical rules:
- No implicit capability takeover: do not “pick the first registrant” or otherwise continue with silently changed behavior. If the required owner is gone/detached, fail with a clear reason/event.
- Auth callbacks must not fail open: on state/verification mismatch, only proceed for an explicit allow-list user action; dismiss/close should behave as cancel (deny).
- Permission grants must be bounded by effective paths: when constraining to a workspace/project root, validate the resolved/real target and ensure it cannot escape the intended boundary (symlinks must be deliberately handled and documented). When granting sandbox writes, never allow read-write to unsafe ancestors (home dir, filesystem root, drive root, or any ancestor that would make most of the system writable).
- Never log secrets by default: any URL/path that can contain OAuth codes, tokens, userinfo, or credentials must be redacted (e.g., log only origin for URLs). In production, keep logging narrow; if you must include details, sanitize them first.

Example (fail-closed auth mismatch):
```ts
if (authNonce !== state) {
  const choice = await vscode.window.showWarningMessage(
    `Could not verify auth response from ${uri.path}. Store the token?`,
    { modal: true },
    "Store"
  );
  if (choice !== "Store") return; // dismiss/esc/click outside => deny
}

// Only proceed after verification or explicit allow-list
if (token) {
  await authService.storeToken(provider, token);
}
```

Example (URL redaction principle):
```ts
export function redactUrlForLog(url: string): string {
  try {
    const u = new URL(url);
    if (u.origin === "null") return `${u.protocol}<redacted>`;
    return u.origin; // drop path/query/userinfo
  } catch {
    return "<invalid url>";
  }
}
```

Apply this standard to any code path that changes who is allowed to act, where data can be read/written, or what sensitive material could leak into logs.