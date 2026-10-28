---
title: Avoid duplicate logic
description: 'Before writing new logic, check whether equivalent functionality already
  exists elsewhere in the codebase (shared utility packages, core services, or sibling
  methods) and reuse it instead of reimplementing it. This applies at multiple levels:'
repository: cline/cline#`sleep 4`
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70979
---

Before writing new logic, check whether equivalent functionality already exists elsewhere in the codebase (shared utility packages, core services, or sibling methods) and reuse it instead of reimplementing it. This applies at multiple levels:

- Cross-package/app duplication: if core or a shared package already implements a capability (e.g. git remote normalization, shell-kind detection), import and reuse it rather than writing a parallel implementation in an app or another module. If a new feature needs to extend that capability, add the extension next to the existing implementation rather than forking it.
- Within-module duplication: when two functions/methods contain near-identical setup or teardown sequences (e.g. `shutdownSession` and `releaseSessionRuntime` both starting with the same three lines and ending with the same shutdown sequence), extract the shared steps into a common helper so each function is left only with its true differences.
- Placement/centralization: when logic is useful to more than one consumer, place it in the layer that respects the dependency graph (e.g. a utility used by both an app and the SDK belongs in core/shared, not duplicated in the app), and route all consumers through that single implementation.

Example refactor pattern:
```ts
// Before: duplicated setup/teardown across two methods
async function shutdownSession(session) {
  this.beginTeardown(session);
  session.pluginCommandsClosing = true;
  emitTaskCompletedOnTeardown(session);
  await abortActiveTurn(session);
  await session.pluginCommandTail;
  await shutdown(session);
  // ...session-specific status/event logic
}

async function releaseSessionRuntime(session) {
  this.beginTeardown(session);
  session.pluginCommandsClosing = true;
  emitTaskCompletedOnTeardown(session);
  await abortActiveTurn(session);
  await session.pluginCommandTail;
  await shutdown(session);
  // ...release-specific logic
}

// After: shared helper holds the common sequence
beginTeardown(session) {
  session.pluginCommandsClosing = true;
  emitTaskCompletedOnTeardown(session);
  this.abortActiveTurn(session);
}

async shutDownSessionRuntime(session) {
  await session.pluginCommandTail;
  await shutdown(session);
}

async function shutdownSession(session) {
  this.beginTeardown(session);
  await this.shutDownSessionRuntime(session);
  // only session-specific status/event logic remains
}

async function releaseSessionRuntime(session) {
  this.beginTeardown(session);
  await this.shutDownSessionRuntime(session);
  // only release-specific logic remains
}
```

Treating duplication as a defect to fix—by reusing existing utilities, extracting shared helpers, and centralizing logic in the correct layer—keeps the codebase smaller, easier to maintain, and less prone to divergent bug fixes.