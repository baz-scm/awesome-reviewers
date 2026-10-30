---
title: Reduce duplication, clarify intent
description: Before writing new logic, check whether it already exists in a shared
  package or nearby module (e.g. a shell-type check, a git-remote normalizer) and
  reuse it instead of re-implementing it in a new file or app. When two or more functions
  repeat the same multi-line sequence (teardown steps, discard/emit/record flows,
  etc.), extract the shared steps into one...
repository: cline/cline#"><b>zze3729958
label: Code Style
language: TypeScript
comments_count: 9
repository_stars: 71067
---

Before writing new logic, check whether it already exists in a shared package or nearby module (e.g. a shell-type check, a git-remote normalizer) and reuse it instead of re-implementing it in a new file or app. When two or more functions repeat the same multi-line sequence (teardown steps, discard/emit/record flows, etc.), extract the shared steps into one well-named helper or module and leave only the true differences in each caller — but don't force an extraction for a two-line, self-explanatory duplicate shared by only two adjacent call sites, as that can add more indirection than it removes; wait for a third real use case.

Also watch for duplicated *shapes* of control flow: if you find yourself repeatedly branching on a flag (`outputMode === "json"`, a growing `if/else` ladder) to decide how to report something, replace the branching with a small role/strategy abstraction (e.g. a `RunOutputter` created once with `JsonRunOutputter`/`ConsoleRunOutputter` implementations) so each branch becomes a straight-line call with a clear method name. Similarly, avoid stacking positional boolean parameters (`load(true, true)`), which are unreadable at the call site and easy to swap by mistake; use a destructured options object with named, defaulted fields instead (`load({ refresh: true, userInitiated: true })`).

If a chunk of new code is specific to one feature/tool and is large, put it in its own module rather than bolting it onto a shared, general-purpose file — this keeps shared files focused and makes feature-specific logic easy to find and test independently.