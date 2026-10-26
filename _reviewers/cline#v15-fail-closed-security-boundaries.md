---
title: Fail-closed Security Boundaries
description: 'Security-sensitive flows must be fail-closed: if authorization/ownership
  cannot be proven, do not “fall through” to a token store, silent takeover, or unsafe
  grants; instead, require an explicit compatible/allowed action and deny by default.'
repository: cline/cline#v15
label: Security
language: TypeScript
comments_count: 5
repository_stars: 70877
---

Security-sensitive flows must be fail-closed: if authorization/ownership cannot be proven, do not “fall through” to a token store, silent takeover, or unsafe grants; instead, require an explicit compatible/allowed action and deny by default.

Apply this consistently:
- **No implicit fallback/transfer**: if the intended owner can’t be resolved (disconnect/detach/cancelled) or a capability takeover isn’t explicitly compatible, fail clearly and emit telemetry.
- **Explicit allow-list on auth callbacks**: treat any non-deliberate outcome (e.g., prompt dismissed/undefined) as denial; state-mismatch must not store tokens.
- **Secrets-safe logging**: in production, log only safe primitives; never include credential-bearing URLs/paths; redact URLs to origin (and avoid free-text scrubbing that can be bypassed).
- **Sandbox/path boundaries**: validate real/canonical paths; fail closed if read-write grants include filesystem roots, home directory, or ancestors.

Example (auth mismatch: denial by default):
```ts
if (authService.authNonce !== state) {
  const choice = await vscode.window.showWarningMessage(
    `Authentication response could not be verified. Store the token from ${uri.path}?`,
    { modal: true },
    "Store"
  );
  if (choice !== "Store") return; // dismissed/undefined => deny
}
```

Example (URL logging: redact instead of echoing):
```ts
function redactUrlForLog(url: string) {
  try { return new URL(url).origin; } catch { return "<invalid url>"; }
}
// Logger: never log full URLs from errors/inputs in production.
```