---
title: Fail-closed, least-privilege boundaries
description: When code enforces a security or trust boundary (file-system sandboxes,
  path containment, network policy, auth confirmations), default to the most restrictive
  outcome and grant only what is strictly required, verified precisely.
repository: cline/cline;
label: Security
language: TypeScript
comments_count: 11
repository_stars: 70964
---

When code enforces a security or trust boundary (file-system sandboxes, path containment, network policy, auth confirmations), default to the most restrictive outcome and grant only what is strictly required, verified precisely.

Concretely:
- Never grant write/trust based on an unvalidated or loosely-derived root. Resolve real paths (through symlinks) and check containment with exact prefix/child logic (e.g. reject only when a relative path is `..` or starts with `../`/`..\\`), not substring or heuristic matching. A sandbox or project-explorer root is not itself a trust boundary unless the connection/caller requesting it has already been authenticated/authorized.
- Grant the minimum filesystem/network access needed for the task. Don't seed read-write access from an arbitrary `cwd` without checking it isn't a volume root, home directory, or ancestor of one. Scope caches/tmp dirs explicitly rather than widening the whole working directory tree. Only request network ingress/egress capabilities a feature actually needs (e.g. don't request loopback ingress on a platform whose sandbox tier rejects it and fails closed as a result).
- Treat allow/deny lists for sensitive data (filenames, path patterns) as inherently incomplete; expand them when gaps are found, but do not advertise them as comprehensive protection, and prefer structural checks over pattern matching where possible.
- When a security check is ambiguous or inconclusive (e.g. a confirmation dialog is dismissed, a state/nonce can't be verified), the code must deny/abort by default. Only an explicit, affirmative action should allow a sensitive operation to proceed — never let `undefined`/dismissed results fall through to the "allow" branch:

```ts
// Wrong: dismissing the dialog (undefined) falls through to allow.
if (userConfirmation === "Cancel") return

// Right: only an explicit affirmative action proceeds.
if (userConfirmation !== "Store") return
```

Apply this standard whenever introducing or reviewing code that decides what a user, process, or remote caller is allowed to read, write, or execute.