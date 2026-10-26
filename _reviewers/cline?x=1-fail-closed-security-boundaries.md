---
title: Fail-Closed Security Boundaries
description: 'Security checks must be explicit and fail closed when boundaries can’t
  be proven.


  Apply this standard everywhere you:

  - Accept auth/callback input: never treat “user confirmation” as a security boundary
  unless the control flow is an exact allow-list and the underlying nonce/state is
  actually anti-forgery (short-lived/rotated).'
repository: cline/cline?x=1
label: Security
language: TypeScript
comments_count: 10
repository_stars: 70861
---

Security checks must be explicit and fail closed when boundaries can’t be proven.

Apply this standard everywhere you:
- Accept auth/callback input: never treat “user confirmation” as a security boundary unless the control flow is an exact allow-list and the underlying nonce/state is actually anti-forgery (short-lived/rotated).
- Transfer/resolve capabilities or ownership: never silently pick the first registrant or fallback behavior that can change running behavior; require explicit compatible takeover or fail the request.
- Grant filesystem/sandbox write access: resolve real paths (incl. symlinks) and reject overly broad grants (filesystem roots, volumes/drives, home, or ancestors of them). Only allow narrowly-scoped write roots and specific file types.
- Log user-controlled or credential-bearing data: in production, restrict log fields and redact URLs to origin (never query/path/userinfo). Don’t echo expanded env-resolved URLs or secrets via error messages.

Code example (auth mismatch should not store on dismiss):
```ts
if (authService.authNonce !== state) {
  const res = await vscode.window.showWarningMessage(
    `The authentication response could not be verified. Store the token returned from ${uri.path}?`,
    { modal: true },
    "Store",
    "Cancel",
  );

  // Fail closed unless the user explicitly clicked the allow-listed button.
  if (res !== "Store") return;
}
// proceed only after verified state/nonce
```

Code example (URL redaction for logs):
```ts
export function redactUrlForLog(raw: string): string {
  try {
    const u = new URL(raw);
    if (u.origin === "null") return `${u.protocol}<redacted>`;
    return u.origin; // origin only; never query/path/userinfo
  } catch {
    return "<invalid url>";
  }
}
```

Checklist for PRs:
- Boundary check paths: “What happens on mismatch/dismiss/disconnect?” must fail closed.
- Nonces/states: confirm the nonce/state is actually anti-forgery (rotated/short-lived/validated), not just a UI prompt trigger.
- Filesystem/security domains: resolve real paths and enforce allowed roots + strict file-type allow-lists; deny root/home/drive ancestors for write.
- Logging: ensure production logs can’t contain tokens/secrets/credential-bearing URLs (use origin-only redaction and narrow serializers).