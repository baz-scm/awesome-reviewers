---
title: Fail-Closed Security Boundaries
description: 'Adopt a single standard: **security boundaries must be explicit and
  fail closed, and secrets must never be emitted or implicitly retained.** Concretely:'
repository: cline/cline#v2
label: Security
language: TypeScript
comments_count: 13
repository_stars: 70861
---

Adopt a single standard: **security boundaries must be explicit and fail closed, and secrets must never be emitted or implicitly retained.** Concretely:

1) Ownership/capability/auth must not “silently transfer”
- Never select an arbitrary registrant/participant when multiple candidates exist.
- If the owner disappears or auth verification fails, **stop the operation** with a clear user-facing reason and emit telemetry.

2) Auth callback state checks must be non-bypassable
- If `state`/nonce verification fails, do **not** proceed based on a user dismissible prompt.
- Ensure nonces are short-lived/rotated and that “already authorized” logic depends on verified server state.

Example pattern (fail closed):
```ts
if (expectedState !== state) {
  // Do not store token; do not rely on user dismiss/close.
  vscode.window.showWarningMessage("Authentication could not be verified.", { modal: true });
  return; // always cancel
}
```

3) Sandbox/filesystem grants must be validated with resolved real paths
- Validate that write grants are not an ancestor of home/root, not a filesystem root/volume, and not overly broad.
- Resolve symlinks/real paths and fail closed when the grant scope is unsafe.

4) Treat logs/errors as public output
- In production, only log safe primitives; avoid serializing objects/Errors that may contain secrets.
- Never build error messages that concatenate credential-bearing URLs/strings.
- Redact URLs to origin (or scheme-only for non-hierarchical/file-like) before logging.

5) Untrusted paths/files need containment
- Enforce “inside root” checks and get the edge cases right (e.g., `..` handling).
- Keep sensitive-file protections broad enough to cover common credential stores.

Applying this consistently prevents the recurring failures shown here: silent capability takeovers, fail-open auth flows, unsafe sandbox write boundaries, and accidental secret leakage via logs/errors/paths.