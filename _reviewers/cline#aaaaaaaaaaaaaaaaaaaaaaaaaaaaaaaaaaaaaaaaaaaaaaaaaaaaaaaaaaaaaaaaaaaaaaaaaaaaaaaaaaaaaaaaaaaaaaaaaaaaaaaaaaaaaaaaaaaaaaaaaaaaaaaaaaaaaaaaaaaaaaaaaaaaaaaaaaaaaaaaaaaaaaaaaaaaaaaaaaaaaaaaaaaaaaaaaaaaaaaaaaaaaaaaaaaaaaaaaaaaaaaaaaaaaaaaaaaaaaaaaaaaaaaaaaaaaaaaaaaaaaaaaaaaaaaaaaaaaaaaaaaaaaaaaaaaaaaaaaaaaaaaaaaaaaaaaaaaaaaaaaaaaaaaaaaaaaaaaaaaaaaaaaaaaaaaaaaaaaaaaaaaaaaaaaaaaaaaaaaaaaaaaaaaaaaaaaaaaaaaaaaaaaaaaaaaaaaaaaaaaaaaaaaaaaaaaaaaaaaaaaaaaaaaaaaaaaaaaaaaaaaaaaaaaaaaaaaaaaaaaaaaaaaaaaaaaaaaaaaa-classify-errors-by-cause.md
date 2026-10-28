---
title: Classify errors by cause
description: 'Don''t let a single catch block collapse every failure into the same
  outcome. Before deciding how to react, inspect what actually went wrong — the exit
  code and stderr text, the error''s type/instance, the HTTP status, or the specific
  message — and route each distinct cause to the right behavior: treat truly expected
  conditions as empty/skipped, let transient...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Error Handling
language: TypeScript
comments_count: 8
repository_stars: 70964
---

Don't let a single catch block collapse every failure into the same outcome. Before deciding how to react, inspect what actually went wrong — the exit code and stderr text, the error's type/instance, the HTTP status, or the specific message — and route each distinct cause to the right behavior: treat truly expected conditions as empty/skipped, let transient or unrelated failures propagate as real errors, and only fall back silently when you've confirmed that's what happened.

Several regressions came from assuming one error shape meant one thing:
- Exit code 128 from `git status` was treated as "not a repository" unconditionally; any other fatal git error (e.g. a corrupted repo) was silently mapped to the same "unknown" state instead of being distinguished. Fix: also check that stderr says "not a git repository" before taking that branch.
- `git show` failures during diff preview were treated as "file doesn't exist" for any rejection, including a `maxBuffer` overflow — producing a fake deletion instead of surfacing the real error. Fix: only treat it as missing when git reports "does not exist" / "not in index" / "invalid object", otherwise propagate.
- A generic `catch` around environment capture made `startSession` fail outright on any size/shape violation, when the safer behavior is to log and fall back to the previous inheritance path.
- A spawn `ENOENT` was reported identically for "binary not on PATH" and "working directory doesn't exist" — two very different problems that call for different user-facing guidance.
- A regex meant to detect "session lost" errors only matched one of the two transport error shapes the SDK actually throws, silently failing to recover the common case.

```ts
// Bad: one shape assumed for every failure
try {
  await git(root, ["status", ...]);
} catch {
  return undefined; // treats every git failure as "not a repo"
}

// Good: inspect the actual cause before choosing the outcome
try {
  await git(root, ["status", ...]);
} catch (error) {
  return isNotARepositoryError(error) ? undefined : "unknown";
}
```

When writing a catch block (or a `.catch()`/fallback branch), ask: "what are the different reasons this could fail, and does each deserve the same response?" If not, branch on concrete signals instead of defaulting everyone into the same path. This keeps expected conditions (missing file, no repo) cheap to handle while real failures (corrupted state, size limits, unexpected server responses) stay visible instead of being disguised as something benign.