---
title: Fail-Closed Secret Safety
description: 'Security rules should be fail-closed: when authentication, capability
  ownership, or boundary validation is uncertain, the system must stop rather than
  continue—and logs must never leak credentials.'
repository: cline/cline#v26
label: Security
language: TypeScript
comments_count: 14
repository_stars: 70893
---

Security rules should be fail-closed: when authentication, capability ownership, or boundary validation is uncertain, the system must stop rather than continue—and logs must never leak credentials.

Apply these standards:
1) Auth callbacks: never store tokens on state/nonce mismatch unless it’s an explicit allow-list confirmation.
   - Dismiss/close/ESC should be treated as rejection.
   - Use a nonce/state that’s generated per auth request (or within a short-lived set), not a single long-lived value.
2) Secret-safe logging (production):
   - Use an allow-list formatter: keep only safe primitives (numbers/booleans) and vetted error messages; drop or heavily limit strings/objects in production.
   - Redact URLs before logging (at minimum: keep only origin; never log paths/query/userinfo where OAuth codes/tokens often live).
   - Avoid “free-text scrubbers” as a guarantee; instead fix the root (don’t construct messages containing secrets) and redact where unavoidable.
3) Enforce trust boundaries with fail-closed containment:
   - For capability/task execution, do not silently transfer behavior to another client. If the owner disconnects/detaches, fail with a clear message.
   - For sandboxes and filesystem access, resolve real paths and fail closed when write grants target high-risk roots (volume root, home, or ancestors). Test path escaping (e.g., only reject actual “..” traversal prefixes).

Example (auth state mismatch fail-closed + safe URL logging):
```ts
function redactUrlForLog(url: string): string {
  try {
    const u = new URL(url);
    if (u.origin === "null") return `${u.protocol}<redacted>`;
    return u.origin; // origin only
  } catch {
    return "<invalid url>";
  }
}

async function handleAuthCallback(authNonce: string, stateFromUrl: string, uri: URL) {
  if (authNonce !== stateFromUrl) {
    const choice = await vscode.window.showWarningMessage(
      `The authentication response could not be verified. Store the token returned from ${redactUrlForLog(uri.toString())}?`,
      { modal: true },
      "Store",
    );
    // Dismissal/ESC must abort.
    if (choice !== "Store") return;
  }
  // Only store after verified or explicit allow-listed user confirmation.
}
```

Outcome: fewer auth bypasses (no fail-open), no credential-bearing logs, and stronger containment for privileged actions.