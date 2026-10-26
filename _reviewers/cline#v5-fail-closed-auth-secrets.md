---
title: Fail Closed Auth Secrets
description: 'Security standard: **Authentication/authorization decisions must fail
  closed, and any credential-bearing data (tokens, URLs, paths, headers) must be treated
  as hostile—never logged or broadly persisted, and never expanded into wider write
  permissions than intended.**'
repository: cline/cline#v5
label: Security
language: TypeScript
comments_count: 10
repository_stars: 70864
---

Security standard: **Authentication/authorization decisions must fail closed, and any credential-bearing data (tokens, URLs, paths, headers) must be treated as hostile—never logged or broadly persisted, and never expanded into wider write permissions than intended.**

Apply these rules:

1) **Auth callback state mismatches must be fail-closed**
- If `state` doesn’t match (or cannot be verified), do **not** proceed by default.
- If you ask the user, treat “dismiss/esc/close” as **Cancel** by using an explicit allow-list check.
- Prefer a nonce/state model that actually provides CSRF/anti-replay protection; avoid downgrading it into “cosmetic prompting”.

```ts
// Fail-closed pattern
if (authNonce !== state) {
  const choice = await vscode.window.showWarningMessage(
    `Could not verify authentication response. Continue?`,
    { modal: true },
    "Store"
  );
  if (choice !== "Store") return; // dismiss/esc/close => abort
}
// continue only when verified or explicitly allowed
```

2) **Never leak secrets in logs/UI telemetry**
- Redact URLs down to `origin` (or scheme-only when origin is `null`) before logging.
- In production, constrain log arguments to safe types; avoid serializing strings/objects that may contain tokens, codes, keys, or file contents.
- Don’t embed secrets into constructed error messages that are later logged.

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

3) **Least-privilege boundaries must be enforced with real paths**
- When granting write access in a sandbox, validate the resolved/real target paths.
- Refuse to grant writes to volume roots, home directory, or any ancestor that would effectively widen the boundary.
- Treat symlink resolution and ancestor checks as part of the security boundary (fail closed if the containment proof can’t be established).

4) **Credential handling must be explicit and gated**
- Only clear/replace identity fields when you can prove you’re replacing a real OAuth/browser sign-in (e.g., gate on presence of stored OAuth tokens).
- Any GUI/user patch that touches credential-bearing fields (including auth token channels like headers) must correctly classify the entry as “manual” vs “oauth/migration sourced.”

Code reviews should check for: (a) no fail-open auth flows, (b) no secret-bearing logging, (c) sandbox/FS boundaries validated via resolved paths, and (d) credential update logic precisely gated to the scenario being handled.