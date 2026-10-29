---
title: Filesystem boundary enforcement
description: 'Any code that confines file access to a directory (project explorer,
  rule file writers, command sandboxes) must validate the boundary correctly and fail
  safely when that validation is uncertain:'
repository: cline/cline#1
label: Security
language: TypeScript
comments_count: 8
repository_stars: 71024
---

Any code that confines file access to a directory (project explorer, rule file writers, command sandboxes) must validate the boundary correctly and fail safely when that validation is uncertain:

1. Resolve symlinks before checking containment. Compare the canonical (`realpath`) target against the canonical root, not the raw requested path, so a symlink cannot escape the intended directory. Only reject genuine traversal segments (e.g. `..` itself, or `../`/`..\\` prefixes) rather than any path that merely contains `..` as a substring, which would wrongly block legitimate names like `..notes`.

```ts
function assertInsideRoot(root: string, path: string): void {
  const rel = relative(root, path);
  if (rel === ".." || rel.startsWith(`..${sep}`) || isAbsolute(rel)) {
    throw new Error("Path is outside the workspace");
  }
}
```

2. When granting write access for a sandbox (e.g. "only allow edits in project directory"), resolve the real path of the grant and explicitly reject/flag grants that resolve to a volume root, filesystem root, the home directory, or an ancestor of it. A `cwd` of `~` or a drive root must not silently become a fully writable boundary.

3. A path/containment check is a coherence guard, not a trust boundary by itself. Gate the underlying capability (e.g. filesystem RPC commands) on an authenticated/trusted transport connection, and document that the path check exists to keep the tool coherent rather than to enforce security on its own.

4. Prefer failing closed when the security-relevant state can't be determined. If a security setting (e.g. a sandbox toggle) can't be read due to a corrupt or torn file, don't silently fall back to an insecure default as though the setting were off — distinguish "absent" from "unreadable," log/warn on the unreadable case, and keep enforcing the last known-safe state rather than silently disabling protection.

Apply these checks with tests that specifically cover symlink escapes, boundary edge cases (e.g. `..`-prefixed but legitimate names), and corrupted/unreadable state, so a filesystem boundary can't be bypassed or silently disabled.