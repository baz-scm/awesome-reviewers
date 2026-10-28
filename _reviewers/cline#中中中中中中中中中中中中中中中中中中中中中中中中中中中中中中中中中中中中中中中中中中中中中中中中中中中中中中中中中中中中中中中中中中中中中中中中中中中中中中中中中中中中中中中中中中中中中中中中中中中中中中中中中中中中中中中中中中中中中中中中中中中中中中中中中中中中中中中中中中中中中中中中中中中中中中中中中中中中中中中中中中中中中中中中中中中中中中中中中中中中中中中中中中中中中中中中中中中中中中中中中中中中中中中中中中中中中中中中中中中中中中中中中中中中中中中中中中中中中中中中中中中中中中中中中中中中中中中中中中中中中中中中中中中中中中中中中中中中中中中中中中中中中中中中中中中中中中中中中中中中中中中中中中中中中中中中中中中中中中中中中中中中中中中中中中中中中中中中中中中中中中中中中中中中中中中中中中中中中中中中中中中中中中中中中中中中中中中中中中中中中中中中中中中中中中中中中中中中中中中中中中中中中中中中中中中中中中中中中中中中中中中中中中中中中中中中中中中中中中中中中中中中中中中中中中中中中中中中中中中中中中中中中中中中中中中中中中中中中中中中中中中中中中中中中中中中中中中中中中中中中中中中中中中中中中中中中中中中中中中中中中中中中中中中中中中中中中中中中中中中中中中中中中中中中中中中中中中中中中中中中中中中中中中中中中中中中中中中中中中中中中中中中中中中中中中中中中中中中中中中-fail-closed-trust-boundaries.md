---
title: Fail-closed trust boundaries
description: When code enforces a security boundary (sandbox grants, path confinement,
  auth confirmation, feature gating), make the check explicit, resolve it against
  real-world state, and default to the restrictive outcome whenever that state is
  ambiguous or unverifiable.
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Security
language: TypeScript
comments_count: 10
repository_stars: 70984
---

When code enforces a security boundary (sandbox grants, path confinement, auth confirmation, feature gating), make the check explicit, resolve it against real-world state, and default to the restrictive outcome whenever that state is ambiguous or unverifiable.

Concretely:
- Containment checks on paths must resolve symlinks (`realpath`) before comparing, and must reject on exact `..`/`../`/`..\\` boundaries rather than naive prefix matching that false-positives on names like `..notes`. A directory root alone (e.g. a session's `cwd`) is not itself a trust boundary — don't assume a caller is safe just because it chose the root; gate the surrounding transport/connection instead and keep the path check as a coherence guard.
- Sandbox or filesystem grants (e.g. read-write policy for a command sandbox) must never silently include dangerous ancestors: validate that a granted path isn't a volume/filesystem root, the home directory, or an ancestor of it, and fail with a clear message instead of granting broad access.
- Security-relevant settings reads that can fail (torn write, corrupt file, unknown state) must not silently fall back to the permissive default. Distinguish "absent" from "present but unreadable," keep the last-known-good value or fail closed, and surface the degraded state (log/warning) instead of letting protection quietly disappear.
- User-facing confirmation prompts that gate a security-sensitive action (e.g. accepting a mismatched auth callback state) must use an explicit allow-list: only a deliberate, matching response proceeds. Any dismissal, Escape, or unexpected result must be treated as "deny," not as an implicit pass-through. Prefer modal prompts to prevent a dismissal from acting as a default.

Example of the allow-list confirmation pattern:
```ts
if (authService.authNonce !== state) {
    const confirmation = await vscode.window.showWarningMessage(
        "The authentication response could not be verified. Store it anyway?",
        { modal: true },
        "Store",
    )
    if (confirmation !== "Store") {
        return // any dismissal or other result denies
    }
}
```

Apply the same reasoning to write-path containment: resolve the real file path, require it to be a regular file, and only treat it as writable when it is a direct member of an explicitly allowed root (not merely "doesn't start with the root's negation").