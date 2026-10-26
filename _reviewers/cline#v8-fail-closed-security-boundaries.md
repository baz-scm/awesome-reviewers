---
title: Fail-Closed Security Boundaries
description: 'Treat any trust boundary (auth callbacks, capability/session ownership,
  and privileged execution) as *fail-closed*: never proceed when verification is missing/ambiguous,
  and never accept implicit fallback that can change behavior.'
repository: cline/cline#v8
label: Security
language: TypeScript
comments_count: 8
repository_stars: 70867
---

Treat any trust boundary (auth callbacks, capability/session ownership, and privileged execution) as *fail-closed*: never proceed when verification is missing/ambiguous, and never accept implicit fallback that can change behavior.

Practical rules:
1) Enforce security checks with an allow-list, not a “dismiss means continue” pattern.
   - If state/nonce/ownership verification fails, only continue on an explicit affirmative user action.
   - If user confirmation returns `undefined` (dismiss/escape/outside click), abort.
2) Make takeover/ownership behavior explicit.
   - Avoid “first attached registrant wins” or other implicit transfers that can silently alter running-task behavior.
   - If safe transfer compatibility can’t be proven, fail clearly and instrument the reason.
3) Constrain privilege scope and verify real boundaries.
   - For sandbox/filesystem write grants, resolve real paths and refuse dangerous grants (filesystem roots, home directory, or ancestors of them). Fail closed.
   - For any file write based on user paths, resolve symlinks/realpaths and only allow documented file types inside allowed roots.
4) Sanitize secrets in logs and error messages.
   - In production, do not log raw error objects/extra args that may embed URLs/tokens/file contents.
   - Redact URLs to origin (never query/path) and reduce any credential-bearing error text.

Example (auth state mismatch: allow-list + fail-closed):
```ts
if (authService.authNonce !== state) {
  const confirmed = await vscode.window.showWarningMessage(
    `Authentication could not be verified. Store token from ${uri.path}?`,
    { modal: true },
    "Store",
  );
  if (confirmed !== "Store") return; // dismiss/escape/close => undefined => abort
}
```

Outcome: verification failures, unexpected authority changes, unsafe privilege scopes, and potential secret leakage should all result in explicit rejection (and safe, redacted telemetry), not silent continuation.