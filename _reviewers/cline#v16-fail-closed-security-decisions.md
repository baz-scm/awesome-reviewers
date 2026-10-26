---
title: Fail-Closed Security Decisions
description: All security-critical flows must use explicit allow-lists and fail closed
  when verification isn’t provably correct. Avoid silent fallbacks/auto-takeover,
  and never proceed after a security check is ambiguous (e.g., user dismisses a prompt,
  token/state is missing/doesn’t match, capability owner detaches).
repository: cline/cline#v16
label: Security
language: TypeScript
comments_count: 7
repository_stars: 70882
---

All security-critical flows must use explicit allow-lists and fail closed when verification isn’t provably correct. Avoid silent fallbacks/auto-takeover, and never proceed after a security check is ambiguous (e.g., user dismisses a prompt, token/state is missing/doesn’t match, capability owner detaches).

Additionally, treat secrets as hostile data: never log raw URLs/paths/tokens or serialize errors in a way that can include credentials (OAuth codes, userinfo, query params, auth headers).

Apply this standard:
- Auth/CSRF/state/nonce checks: if verification fails, abort unless the code explicitly allows only a deliberate confirmation (and the confirmation must be the allowed return value; dismiss/close must default to cancel).
- Ownership/capability transfer: if the intended owner can’t be verified, do not “select first attached registrant” or transfer/replay implicitly; instead fail clearly and record a security event.
- Sandbox/filesystem/path boundaries: resolve and validate real paths; if the writable boundary is too broad (home/root/ancestor/volume), fail closed.
- Secrets in logs/telemetry: redact by construction (origin-only URLs, no query/fragment/userinfo) and narrow production log arguments.

Example (fail-closed auth callback):
```ts
// Abort unless verification explicitly passes.
if (authService.authNonce !== state) {
  const result = await vscode.window.showWarningMessage(
    `The authentication response could not be verified. Continue?`,
    { modal: true },
    "Continue"
  );
  // Dismiss/close/ESC returns undefined => must fail closed.
  if (result !== "Continue") return;
}
// proceed only when allowed
```

Example (safe URL logging):
```ts
function redactUrlForLog(input: string) {
  try {
    const u = new URL(input);
    if (u.origin === "null") return `${u.protocol}<redacted>`;
    return u.origin; // drop pathname/query/fragment/userinfo
  } catch {
    return "<invalid url>";
  }
}
// Logger in production must omit non-primitive/secret-bearing args.
```