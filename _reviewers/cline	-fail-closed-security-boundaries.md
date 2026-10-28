---
title: Fail-closed security boundaries
description: Any check that decides whether an action is authorized — auth-state validation,
  filesystem sandbox grants, path containment, or user confirmation prompts — must
  fail closed on ambiguity, and must validate against resolved/canonical values rather
  than raw input it trusts implicitly.
repository: "cline/cline\t"
label: Security
language: TypeScript
comments_count: 5
repository_stars: 70947
---

Any check that decides whether an action is authorized — auth-state validation, filesystem sandbox grants, path containment, or user confirmation prompts — must fail closed on ambiguity, and must validate against resolved/canonical values rather than raw input it trusts implicitly.

Two recurring failure patterns to avoid:

1. **Confirmation/approval logic that fails open.** Checking for one "reject" value while treating everything else (including a dismissed dialog, timeout, or unrecognized result) as approval silently grants access on an untrusted path. Always use an explicit allow-list for the approving action and treat anything else as denial:
```ts
// Bad: dismissing the dialog (undefined) falls through to the approved branch
if (userConfirmation === "Cancel") return

// Good: only an explicit, deliberate approval proceeds
const userConfirmation = await vscode.window.showWarningMessage(
    "The authentication response could not be verified. Store the token?",
    { modal: true },
    "Store",
)
if (userConfirmation !== "Store") return
```
This applies equally to anti-forgery tokens (e.g. OAuth `state`/nonce): if a mismatch is downgraded to "ask the user" instead of rejecting outright, the nonce must still be freshly generated/rotated per request and the prompt must make the risk explicit — otherwise the check provides no real protection.

2. **Trust boundaries computed from unresolved or unchecked paths.** A working directory, sandbox root, or "allowed roots" set must be resolved to its real, canonical path and checked against dangerous cases (filesystem/drive roots, the home directory or its ancestors, symlink escapes) before being granted read-write or file-access permissions. If the boundary can't be verified as safe, fail with a clear error instead of silently granting broader access than intended:
```ts
// A session's cwd must not become an unrestricted write grant
const real = realpathSync(cwd)
if (isRootOrHomeAncestor(real)) {
  throw new Error(`Refusing to grant write access to ${real}: too broad a boundary`)
}
```
When a path-confinement check is a secondary "coherence guard" rather than the actual trust boundary, say so in a comment and gate the sensitive operation on the real boundary (e.g. requiring a trusted/authenticated connection) instead of implying the path check alone is sufficient protection.

Apply this standard whenever adding or reviewing code that grants access, confirms a security-relevant action, or establishes a sandbox/containment boundary: enumerate the unsafe cases explicitly, default to denial, and resolve real paths/identities before comparing them.