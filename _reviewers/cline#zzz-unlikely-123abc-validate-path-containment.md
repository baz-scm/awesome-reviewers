---
title: Validate path containment
description: Whenever an operation must stay inside a root directory (a workspace,
  a rules folder, a sandbox grant), the containment check itself must be sound, and
  must not be mistaken for the real trust boundary.
repository: cline/cline#zzz-unlikely-123abc
label: Security
language: TypeScript
comments_count: 6
repository_stars: 71035
---

Whenever an operation must stay inside a root directory (a workspace, a rules folder, a sandbox grant), the containment check itself must be sound, and must not be mistaken for the real trust boundary.

1. Resolve real paths before comparing. Resolve both the root and the candidate path through symlinks (`realpath`) before deciding containment; otherwise a link that points outside the root bypasses the check entirely. If following links is an intentional product choice (e.g. letting users browse linked sibling checkouts), document that explicitly at the check site instead of leaving it ambiguous.

2. Use exact boundary comparisons, not string prefixes. Rejecting `startsWith("..")` or similar naive prefixes misclassifies both ways: it can wrongly flag a sibling like `..notes/` as escaping, and can miss other escape shapes. Compare using path segments (`path.relative` plus a check that the result is `""`, doesn't start with a `..` segment, and isn't absolute), e.g.:
```ts
function assertInsideRoot(root: string, target: string): void {
  const rel = path.relative(root, target);
  if (rel === ".." || rel.startsWith(`..${path.sep}`) || path.isAbsolute(rel)) {
    throw new Error("Path is outside the allowed root");
  }
}
```

3. Don't grant a root that is itself too broad. When a root comes from user/session input (e.g. a sandbox's `cwd`), verify the resolved root isn't a filesystem/volume root, the home directory, or an ancestor of it before treating it as writable or otherwise trusted — granting `cwd` blindly can silently grant the whole home directory or drive.

4. Treat path containment as a coherence guard, not an authorization mechanism. A root-confinement check only ensures the operation stays where it's supposed to; it does not establish who is allowed to invoke the operation. Authorization must be enforced independently (e.g. gating the command on a trusted/authenticated connection) before the path logic ever runs, and comments/docs should not overstate what the containment check alone provides.