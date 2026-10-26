---
title: Fail-Closed Security Boundaries
description: Treat every security-critical decision (auth callbacks, capability ownership/transfer,
  and sandboxed filesystem writes) as a deny-by-default trust boundary.
repository: cline/cline#v9
label: Security
language: TypeScript
comments_count: 10
repository_stars: 70868
---

Treat every security-critical decision (auth callbacks, capability ownership/transfer, and sandboxed filesystem writes) as a deny-by-default trust boundary.

Rules:
1) Authorization/anti-forgery: if verification is missing/invalid/ambiguous, proceed only after an explicit allow-list user action. “Dismissed/undefined/close” must never be interpreted as approval.
2) Ownership/transfer: never silently fall back to “first match” or an attached registrant when transfer compatibility isn’t explicitly guaranteed; fail clearly instead.
3) Sandbox boundaries: validate real filesystem paths used for read-write grants. Resolve real paths and fail closed if grants target filesystem roots, home, or ancestors (or anything that makes the safety boundary effectively whole-machine).
4) Secret exfiltration: redact credentials-bearing URLs in logs (e.g., log only origin/allowed safe parts). In production, narrow logging to non-secret primitives and error-message metadata—do not log full strings/objects that may contain tokens, paths, or OAuth data.

Example (OAuth state mismatch should not fail open):
```ts
if (authService.authNonce !== state) {
  const res = await vscode.window.showWarningMessage(
    `Authentication response could not be verified. Store the token returned from ${uri.path}?`,
    { modal: true },
    "Store"
  );
  // Deny-by-default: only the explicit button proceeds.
  if (res !== "Store") return;
}
```

Example (origin-only URL logging):
```ts
export function redactUrlForLog(url: string): string {
  try {
    const parsed = new URL(url);
    return parsed.origin === "null" ? `${parsed.protocol}<redacted>` : parsed.origin;
  } catch {
    return "<invalid url>";
  }
}
```

Practical checklist for PRs:
- What exact condition allows continuation at a trust boundary? Is it an explicit allow-list?
- Are any “fallback” paths changing behavior silently? If yes, replace with an explicit contract/compat check or fail with a clear error.
- For sandbox/tool execution: what are the resolved, real paths granted for write? Do they ever include roots/home/ancestors?
- Do logs ever include raw URLs, tokens, file contents, or error strings built from untrusted/secret-bearing inputs? If so, redact and narrow production logging.