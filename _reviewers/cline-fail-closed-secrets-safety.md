---
title: Fail-Closed Secrets Safety
description: 'Use fail-closed security boundaries and secret-safe observability by
  default.


  ### 1) Auth/CSRF: never store or act on unverified callbacks

  - Treat `state` (or equivalent anti-forgery token) as a required verification gate.'
repository: CLINE/cline
label: Security
language: TypeScript
comments_count: 12
repository_stars: 70839
---

Use fail-closed security boundaries and secret-safe observability by default.

### 1) Auth/CSRF: never store or act on unverified callbacks
- Treat `state` (or equivalent anti-forgery token) as a required verification gate.
- Confirmation prompts must be *allow-list gated* (only a deliberate affirmative action proceeds); dismiss/close must cancel.
- If verification fails, do not persist tokens, do not update session/provider state, and return a safe error.

Example (deny-by-default, allow only explicit “Store”):
```ts
if (authNonce !== state) {
  const choice = await vscode.window.showWarningMessage(
    `Auth callback could not be verified. Store token returned from ${uri.path}?`,
    { modal: true },
    "Store",
  );
  if (choice !== "Store") return; // fail closed on dismiss
}
// proceed to store token only after verified
```

### 2) Authorization/ownership: never “silently takeover” security-critical actions
- For capabilities/clients/agents/tools, require an explicit compatible takeover contract.
- If the original owner/client is gone/detached, fail the request (do not pick an arbitrary first registrant).

### 3) Credentials/state updates: only override the specific credential channel you intend
- When updating provider auth from user input (e.g., pasted API key), clear/replace only the corresponding stored auth state that would otherwise win.
- Gate token/identity clearing on evidence of an actual sign-in state being replaced; avoid dropping identity for same-account rotations unless you also immediately repair via a follow-up fetch.

### 4) Sandboxes/path access: minimize writable roots and validate real boundaries
- Never grant write access to an entire ancestor like home, filesystem root, or the drive without a strict boundary check.
- Resolve real paths (handle symlinks if intentionally allowed) and fail closed when grants would escape the intended project directory.

### 5) Secret-safe logging: redact by policy, not by call-site hope
- In production, log only narrowly-scoped safe data (e.g., numbers/booleans and safe error *messages*), and never serialize arbitrary error objects/strings that may contain OAuth codes, API keys, file/terminal contents, or credential-bearing URLs.
- Always reduce URLs in logs to origin (or an even safer form) before emitting them.
- Error messages built from user-provided strings can leak secrets: fix at the source (don’t “scrub later”).

### 6) Sensitive-file handling: protect against “unknown filename” secrets
- Filename-only blocklists are incomplete; treat them as best-effort and prefer structural detection (path patterns, known secret directories) plus regression tests for previously missed secret types.
- If you add a sensitive-path list, ensure it has tests for multiple variations and deleted/renamed cases.

Adopt these as team coding standards: **deny-by-default on security checks**, **no silent ownership/credential takeover**, **tight filesystem write boundaries**, and **redaction-first observability**.