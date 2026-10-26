---
title: Fail-Closed Auth and Logs
description: 'When handling authentication/authorization and emitting diagnostics,
  use secure defaults: deny on ambiguity, and never leak secrets.


  **Auth/state rules**'
repository: cline/cline#v30
label: Security
language: TypeScript
comments_count: 14
repository_stars: 70894
---

When handling authentication/authorization and emitting diagnostics, use secure defaults: deny on ambiguity, and never leak secrets.

**Auth/state rules**
- Treat *missing, mismatched, or unverified* auth responses as **rejected by default**.
- If you ask the user to confirm, use an **explicit allow-list** (only proceed on a specific button value). Dismiss/ESC/close must behave like cancel.
- Don’t rely on `state` as a mere UI hint; if `state` is downgraded, add compensating protections (rotating/short-lived nonces or bounded acceptance).

**Logging rules**
- Assume URLs (including paths/query/fragment), userinfo, and free-form errors may contain tokens/keys. In production, log only **redacted** values and narrow the argument types you stringify.
- Prefer “origin-only” or “scheme-only” URL redaction, and avoid printing expanded secrets.

**Containment/credential classification (tie-in)**
- Before writing user-controlled files or granting sandbox write paths, validate *real* path containment and deny dangerous roots.
- When determining whether a UI change is “manual credential entry,” include all credential-carrying channels (e.g., `headers`), not just obvious key fields.

**Example (auth confirmation fail-closed)**
```ts
if (expectedState !== actualState) {
  const choice = await vscode.window.showWarningMessage(
    `Authentication could not be verified. Store the token anyway?`,
    { modal: true },
    "Store"
  );
  if (choice !== "Store") return; // dismiss/esc => cancel
}
```

**Example (safe URL logging)**
```ts
function redactUrlForLog(url: string): string {
  try {
    const u = new URL(url);
    if (u.origin === "null") return `${u.protocol}<redacted>`;
    return u.origin; // drop path/query/fragment
  } catch {
    return "<invalid url>";
  }
}
```