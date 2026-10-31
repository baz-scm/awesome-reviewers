---
title: Eliminate meaningful duplication
description: Before adding new logic, search the codebase (including shared packages)
  for an existing implementation and reuse it rather than writing a parallel version.
  For example, don't hand-roll a PowerShell/shell detector when `getShellKind` from
  `@cline/shared` already does it, and don't build a second Git snapshot/remote-normalization
  path when `git-preflight.ts`...
repository: cline/cline?foo=bar
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 71082
---

Before adding new logic, search the codebase (including shared packages) for an existing implementation and reuse it rather than writing a parallel version. For example, don't hand-roll a PowerShell/shell detector when `getShellKind` from `@cline/shared` already does it, and don't build a second Git snapshot/remote-normalization path when `git-preflight.ts` and `normalizeGitHubRemoteUrl` already provide it — move new Git logic next to the existing implementation instead.

When two methods or call sites share substantial, non-trivial logic (e.g. several steps with matching comments, like the teardown sequence shared by `shutdownSession` and `releaseSessionRuntime`), extract the common steps into a single shared helper so each caller is left only with its genuine differences. This keeps behavior consistent and shrinks the code that must be maintained in two places.

Use judgment on trivial cases: if the duplicated body is only a couple of self-explanatory lines, adjacent in the same file, and used in just two places, extracting a helper can add more indirection than it removes — it's fine to leave it inline until a third call site or more complex logic appears.