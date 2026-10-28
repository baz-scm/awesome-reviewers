---
title: Eliminate duplicate logic
description: Before writing new logic, search for an existing implementation (in the
  same module, in core, or in shared packages) and reuse it rather than re-deriving
  the same behavior in a second place. This applies both to small helpers (e.g. a
  shell-kind check or remote-URL normalizer that already lives in `@cline/shared`
  or `@cline/core`) and to larger...
repository: "cline/cline\t"
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70947
---

Before writing new logic, search for an existing implementation (in the same module, in core, or in shared packages) and reuse it rather than re-deriving the same behavior in a second place. This applies both to small helpers (e.g. a shell-kind check or remote-URL normalizer that already lives in `@cline/shared` or `@cline/core`) and to larger near-duplicate code paths (e.g. two teardown methods that both set up the same flags, abort a turn, and shut down the same subsystems with matching comments).

When duplication is found:
- If the duplicate is a utility already exported elsewhere, delete the local copy and import the shared one instead of re-implementing it.
- If two functions share a multi-step sequence, factor the shared steps into one helper (or common base method) that both call, leaving each function with only its genuinely distinct logic.
- If logic is duplicated across an app and the core/SDK layer, move the canonical implementation into core (respecting the dependency direction: apps may depend on core, never the reverse) and have the app import from there.

Example refactor of near-identical teardown paths:

```ts
private beginTeardown(session: Session) {
  session.pluginCommandsClosing = true;
  this.emitTaskCompletedOnTeardown(session);
  this.abortActiveTurn(session);
}

private async shutDownSessionRuntime(session: Session) {
  await session.pluginCommandTail;
  await this.shutdownAgentRuntimeAndSandbox(session);
}

async shutdownSession(session: Session, reason: EndReason) {
  this.beginTeardown(session);
  await this.shutDownSessionRuntime(session);
  // session-specific: persist wait, status write, `ended` event
}

async releaseSessionRuntime(session: Session) {
  this.beginTeardown(session);
  await this.shutDownSessionRuntime(session);
  // release-specific logic only
}
```

This keeps a single source of truth, reduces the surface area for bugs when behavior changes, and makes it obvious at review time what is actually different between similar-looking code paths.</description>
</invoke>
