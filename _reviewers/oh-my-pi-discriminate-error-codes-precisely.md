---
title: Discriminate error codes precisely
description: When catching errors from syscalls, spawned processes, or optional APIs,
  never collapse distinct failure modes into one generic catch. Check the specific
  error code/condition and handle only the exact case you mean to special-case; let
  anything else either propagate or be reported with its own precise status, instead
  of silently mapping it onto an unrelated...
repository: can1357/oh-my-pi
label: Error Handling
language: JavaScript
comments_count: 5
repository_stars: 37317
---

When catching errors from syscalls, spawned processes, or optional APIs, never collapse distinct failure modes into one generic catch. Check the specific error code/condition and handle only the exact case you mean to special-case; let anything else either propagate or be reported with its own precise status, instead of silently mapping it onto an unrelated outcome.

Concretely:
- Match on exact error codes (e.g. `ENOENT`/`ENOTDIR` for "missing") rather than catching broadly and assuming one meaning. A permission error (`EACCES`) or I/O error on a `stat()` is not the same as "doesn't exist" and should surface as its own failure/reason (e.g. "inaccessible") rather than being treated as "not present".
- When probing whether an external binary is usable, enumerate the specific spawn errors that mean "cannot start" (e.g. `ENOENT`, `ENOEXEC`, `EACCES`) and treat only those as the expected condition; any other error should propagate so it isn't masked.
- Distinguish truly benign races (e.g. a file not yet created when a concurrent check runs) from real failures — catch only the specific error code that race implies (`ENOENT`) and treat it as a no-op, not as a hard error.
- When calling an optional or version-dependent API that might be missing (e.g. a native binding absent in an older build), guard the call explicitly and fall back gracefully instead of letting a missing-function error crash the whole module/operation.

Example pattern:
```js
try {
  await fs.promises.stat(path);
} catch (error) {
  if (error?.code === "ENOENT" || error?.code === "ENOTDIR") {
    return { status: "missing" };
  }
  // Don't swallow EACCES/EIO/etc. as "missing" — report distinctly.
  return { status: "inaccessible", error };
}
```

Applying this discipline prevents misleading outcomes (e.g. reporting "no hook" when a hook exists but is unreadable, or crashing on an unrelated race) and makes error messages and recovery behavior accurate and actionable.