---
title: Eliminate duplicated logic
description: Before writing new logic, search the codebase (including shared/core
  packages) for an existing implementation and reuse it rather than re-deriving the
  same behavior in a new file. For example, a shell-kind check or a git-remote normalizer
  that already exists in `@cline/shared`/`@cline/core` should be imported, not reimplemented
  with slightly different code.
repository: "cline/cline\r\n"
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 70946
---

Before writing new logic, search the codebase (including shared/core packages) for an existing implementation and reuse it rather than re-deriving the same behavior in a new file. For example, a shell-kind check or a git-remote normalizer that already exists in `@cline/shared`/`@cline/core` should be imported, not reimplemented with slightly different code.

When you notice two or more methods carrying out the same steps (same structure, same comments, same order of operations) with only small differences, factor the common body into a single shared method and leave each caller with only its real delta. For instance, instead of `shutdownSession` and `releaseSessionRuntime` each repeating teardown setup, emit, and shutdown steps:

```ts
private beginTeardown(session: ActiveSession): void {
  session.shuttingDown = true;
  this.discardPendingPrompts(session, "session_teardown");
}

private async shutDownSessionRuntime(session: ActiveSession): Promise<void> {
  // shared plugin/agent/runtime/sandbox shutdown steps
}

async shutdownSession(...) {
  this.beginTeardown(session);
  await this.shutDownSessionRuntime(session);
  // status write + "ended" event specific to this path
}

async releaseSessionRuntime(...) {
  this.beginTeardown(session);
  await this.shutDownSessionRuntime(session);
  // runtime release specific to this path
}
```

Also place cross-cutting logic (e.g. git plan/preview helpers, session title resolution) in the correct shared package so it has a single owner and respects the dependency direction (apps may depend on core/shared, never the reverse). This avoids two implementations silently drifting apart, reduces the surface area to maintain, and makes the real differences between near-duplicate code paths visible to reviewers.