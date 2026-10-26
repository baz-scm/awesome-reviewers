---
title: Fail-closed Security Boundaries
description: When implementing security-sensitive flows, use explicit, least-privilege
  boundaries and fail closed on any ambiguity. Dismissals, missing context, and “unknown”
  states must never fall back to behavior that continues an operation.
repository: cline/cline#v7
label: Security
language: TypeScript
comments_count: 15
repository_stars: 70865
---

When implementing security-sensitive flows, use explicit, least-privilege boundaries and fail closed on any ambiguity. Dismissals, missing context, and “unknown” states must never fall back to behavior that continues an operation.

Apply this standard:
- **Auth/callbacks:** If a verification check fails (e.g., OAuth `state` mismatch), only continue on an explicit allow-list user confirmation. Treat `undefined`/dismiss/close as **cancel** (no token persistence).
- **Authorization/capability routing:** Never “silently” pick an arbitrary registrant/owner as a fallback. If a safe transfer contract isn’t explicitly established, fail the request and emit telemetry.
- **Sandbox/file access:** Validate containment with **real paths**. Reject filesystem grants when they include volume roots or ancestors that effectively widen the boundary (e.g., granting read-write to `cwd` when `cwd` is `/` or a home/drive ancestor). Prefer allowlists of specific directories.
- **Secrets & logs:** Assume inputs (URLs, paths, error messages) may contain secrets. In production, redact credential-bearing URLs (e.g., keep only `origin`), and log only safe primitives. Never log credential-bearing strings as-is.

Example (auth callback fail-closed):
```ts
if (authService.authNonce !== state) {
  const decision = await vscode.window.showWarningMessage(
    'Authentication response could not be verified. Continue only if you started this sign-in?',
    { modal: true },
    'Store',
  );
  // FAIL CLOSED: dismiss/esc/close => undefined => do not store token
  if (decision !== 'Store') return;
}

if (token) {
  // safe to persist only after passing the boundary
  await authService.storeToken(token);
}
```

Example (secret-safe logging):
```ts
export function redactUrlForLog(url: string): string {
  try {
    const u = new URL(url);
    return u.origin === 'null' ? `${u.protocol}<redacted>` : u.origin;
  } catch {
    return '<invalid url>';
  }
}

// Production: log only safe args; never dump arbitrary objects/errors/strings that may include secrets.
```