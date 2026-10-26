---
title: Fail-closed Security Gates
description: Security-sensitive code must enforce *deny-by-default*, explicit allow-lists,
  and least-privilege—never downgrade verification to “best effort” UX, and never
  let credentials leak via logs/diagnostics.
repository: cline/cline#v3
label: Security
language: TypeScript
comments_count: 9
repository_stars: 70863
---

Security-sensitive code must enforce *deny-by-default*, explicit allow-lists, and least-privilege—never downgrade verification to “best effort” UX, and never let credentials leak via logs/diagnostics.

Apply these rules:
1) Auth/state verification: proceed only on an explicit affirmative action.
- If a security check fails, treat “dismissed/undefined” as failure.
- Don’t rely on a long-lived nonce or on UI confirmation as the security boundary; keep anti-forgery guarantees real and short-lived.

```ts
// Auth callback: state mismatch must not fail open.
if (authNonce !== state) {
  const choice = await vscode.window.showWarningMessage(
    `The authentication response could not be verified. Store the token returned from ${uri.path}?`,
    { modal: true },
    "Store",
  );
  if (choice !== "Store") return; // dismiss/esc/close => deny
}
```

2) Secret hygiene in logs:
- Redact URLs before logging (keep only origin, or scheme for non-hierarchical schemes).
- In production, log only safe primitives (numbers/booleans) and error names/messages that cannot contain secrets.

```ts
export function redactUrlForLog(url: string): string {
  try {
    const u = new URL(url);
    if (u.origin === "null") return `${u.protocol}<redacted>`;
    return u.origin;
  } catch {
    return "<invalid url>";
  }
}
```

3) Sandbox/permission hardening:
- Ensure write permissions are limited to approved directories.
- Deny or tighten policies when any read-write grant includes filesystem roots, home directory, or ancestors of them.
- Resolve/validate real paths to prevent boundary bypass (e.g., via symlink/realpath tricks).

Outcome: auth failures can’t be bypassed by UI dismissal, credentials don’t surface in logs, and sandbox write scopes remain tightly bounded.