---
title: Fail-Closed Security Boundaries
description: 'Use secure-by-default boundaries: when authenticity/ownership is uncertain,
  abort (fail closed), and when handling diagnostics, assume data may contain secrets.'
repository: cline/cline#v4
label: Security
language: TypeScript
comments_count: 9
repository_stars: 70864
---

Use secure-by-default boundaries: when authenticity/ownership is uncertain, abort (fail closed), and when handling diagnostics, assume data may contain secrets.

**Rules**
1) **Auth/verification gates must fail closed**
- Never “proceed on dismissal/undefined”. Treat any non-explicit user consent as refusal.
- Prefer an allow-list (e.g., only proceed when the user clicks a specific affirmative button).

```ts
if (authService.authNonce !== state) {
  const choice = await vscode.window.showWarningMessage(
    'The authentication response could not be verified. Store the token returned from this URL?',
    { modal: true },
    'Store'
  );
  if (choice !== 'Store') return; // fail closed on undefined/dismiss/cancel
}
// proceed to store token only here
```

2) **Sandbox/filesystem grants require strict validation**
- Resolve real paths and ensure read-write grants never include volume roots, the entire home directory, or ancestors of them.
- Boundary checks must precisely reject true traversal escapes (tighten `..` handling), and document any intentional symlink behavior.

3) **Secrets-safe logging by default**
- In production: avoid logging strings/objects/stack traces where credentials or OAuth codes commonly appear.
- Redact URLs for logs: reduce to `origin` (and avoid paths/query/userinfo).

```ts
// Example usage at call sites
Logger.info(`Opening browser: ${redactUrlForLog(url)}`);
```

4) **Ownership/capability transfers must be explicit**
- Never silently transfer behavior by “first matching registrant” when capability contracts may differ.
- If the intended owner is disconnected/detached, fail clearly (optionally with structured telemetry), rather than replaying or transferring implicitly.

Applying these consistently prevents: auth token binding regressions, sandbox escape by overly-broad write grants, path traversal edge cases, and credential leakage via logs.