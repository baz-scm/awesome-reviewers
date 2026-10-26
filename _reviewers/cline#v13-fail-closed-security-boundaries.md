---
title: Fail-Closed Security Boundaries
description: 'Enforce security boundaries by default: when a trust signal is missing/ambiguous,
  the safe action must be to stop (or fail) rather than continue.


  1) Auth / anti-forgery: fail closed'
repository: cline/cline#v13
label: Security
language: TypeScript
comments_count: 9
repository_stars: 70874
---

Enforce security boundaries by default: when a trust signal is missing/ambiguous, the safe action must be to stop (or fail) rather than continue.

1) Auth / anti-forgery: fail closed
- Treat “prompt dismissed/closed/undefined” as a refusal.
- Only proceed on an explicit allow-list user action (e.g., the exact button label).
- Do not downgrade CSRF/state into a best-effort UX check; state must remain a meaningful anti-forgery boundary (rotated/short-lived as appropriate).

Example (state mismatch callback):
```ts
if (authService.authNonce !== state) {
  const userChoice = await vscode.window.showWarningMessage(
    `Authentication response could not be verified. Store the token returned from ${uri.path}?`,
    { modal: true },
    "Store",
  );

  // IMPORTANT: any dismiss => undefined/null => abort
  if (userChoice !== "Store") return;
}

// proceed to store token only after verified boundary
if (token) { /* store */ }
```

2) Ownership / trust gates: fail clearly
- Remove silent fallbacks that change behavior (e.g., capability takeover by “first registrant” or replaying requests) unless you have an explicit, compatible takeover contract.
- Gate sensitive operations on the intended trusted origin/connection and define the containment scope (e.g., workspace root) precisely.

3) Least privilege + input validation
- Validate paths against the allowed root with tests for traversal edge cases.
- Ensure sandbox filesystem grants cannot accidentally expand to home directories, drive roots, or ancestors of the intended project boundary (fail closed if realpaths escape).

4) Secrets hygiene in logs/telemetry
- Redact/sanitize URLs (including OAuth codes and credentials) and avoid logging paths/headers/tokens in production.
- Production logging should be narrow: avoid including arbitrary objects/strings and never rely on per-call-site scrubbing when a central safe formatter can enforce policy.

Apply these as review gate criteria: if the code continues on an ambiguous trust outcome, or logs potentially secret data, or grants broader-than-intended filesystem access, it should be rejected or revised before merge.