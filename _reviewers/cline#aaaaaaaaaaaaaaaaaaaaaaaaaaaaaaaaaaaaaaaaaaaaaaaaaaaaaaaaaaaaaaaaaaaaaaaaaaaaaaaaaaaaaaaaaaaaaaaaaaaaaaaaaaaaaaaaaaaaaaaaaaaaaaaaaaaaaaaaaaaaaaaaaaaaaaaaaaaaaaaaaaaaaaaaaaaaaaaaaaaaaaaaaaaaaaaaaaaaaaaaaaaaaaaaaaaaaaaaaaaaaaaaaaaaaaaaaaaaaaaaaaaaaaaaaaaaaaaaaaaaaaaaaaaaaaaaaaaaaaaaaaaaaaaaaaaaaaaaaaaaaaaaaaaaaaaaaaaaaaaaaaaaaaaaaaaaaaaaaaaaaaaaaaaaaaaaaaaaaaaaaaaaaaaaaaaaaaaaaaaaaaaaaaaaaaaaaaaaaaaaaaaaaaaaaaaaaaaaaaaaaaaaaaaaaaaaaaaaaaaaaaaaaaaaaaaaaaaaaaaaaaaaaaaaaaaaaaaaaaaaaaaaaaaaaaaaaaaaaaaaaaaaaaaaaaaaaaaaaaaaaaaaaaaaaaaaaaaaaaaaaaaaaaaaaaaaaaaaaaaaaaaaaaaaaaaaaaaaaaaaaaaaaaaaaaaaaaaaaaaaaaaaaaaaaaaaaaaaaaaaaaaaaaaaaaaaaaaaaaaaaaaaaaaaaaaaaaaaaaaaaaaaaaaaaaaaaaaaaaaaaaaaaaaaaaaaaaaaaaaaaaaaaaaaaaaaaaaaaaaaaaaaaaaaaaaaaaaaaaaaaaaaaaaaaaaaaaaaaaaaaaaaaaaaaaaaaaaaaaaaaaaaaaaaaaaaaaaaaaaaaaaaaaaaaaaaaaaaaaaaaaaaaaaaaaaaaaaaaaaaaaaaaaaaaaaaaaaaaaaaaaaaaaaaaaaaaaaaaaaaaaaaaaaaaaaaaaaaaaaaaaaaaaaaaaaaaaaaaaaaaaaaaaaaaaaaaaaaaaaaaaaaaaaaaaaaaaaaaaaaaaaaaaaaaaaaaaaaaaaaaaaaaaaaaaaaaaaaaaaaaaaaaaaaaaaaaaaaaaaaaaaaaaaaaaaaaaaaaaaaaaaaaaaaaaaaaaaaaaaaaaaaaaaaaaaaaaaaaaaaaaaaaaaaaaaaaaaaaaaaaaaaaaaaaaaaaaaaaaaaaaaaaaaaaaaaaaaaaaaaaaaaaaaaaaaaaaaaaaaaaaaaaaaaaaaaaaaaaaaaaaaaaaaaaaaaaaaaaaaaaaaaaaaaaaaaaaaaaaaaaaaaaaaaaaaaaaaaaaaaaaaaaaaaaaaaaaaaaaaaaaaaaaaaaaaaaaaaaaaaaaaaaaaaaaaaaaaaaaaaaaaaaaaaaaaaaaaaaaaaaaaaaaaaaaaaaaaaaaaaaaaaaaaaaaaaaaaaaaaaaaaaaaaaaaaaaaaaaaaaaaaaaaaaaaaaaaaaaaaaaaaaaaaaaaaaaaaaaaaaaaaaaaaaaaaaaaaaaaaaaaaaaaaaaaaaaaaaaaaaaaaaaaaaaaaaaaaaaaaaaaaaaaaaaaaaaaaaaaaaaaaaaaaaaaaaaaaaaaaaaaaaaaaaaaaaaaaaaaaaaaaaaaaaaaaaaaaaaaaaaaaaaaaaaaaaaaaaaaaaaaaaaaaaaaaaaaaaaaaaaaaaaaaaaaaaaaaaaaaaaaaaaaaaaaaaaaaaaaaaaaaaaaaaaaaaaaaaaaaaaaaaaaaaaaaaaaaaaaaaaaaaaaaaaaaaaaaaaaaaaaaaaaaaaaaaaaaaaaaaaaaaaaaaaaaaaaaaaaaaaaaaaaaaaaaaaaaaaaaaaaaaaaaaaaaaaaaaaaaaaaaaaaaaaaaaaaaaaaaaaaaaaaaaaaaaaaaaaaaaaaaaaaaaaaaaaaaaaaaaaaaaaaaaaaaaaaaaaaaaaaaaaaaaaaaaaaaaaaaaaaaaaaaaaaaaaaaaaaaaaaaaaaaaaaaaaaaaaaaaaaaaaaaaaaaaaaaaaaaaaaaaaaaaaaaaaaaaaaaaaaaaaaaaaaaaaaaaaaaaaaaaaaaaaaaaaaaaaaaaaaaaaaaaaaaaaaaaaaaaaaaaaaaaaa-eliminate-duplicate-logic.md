---
title: Eliminate duplicate logic
description: When the same logic (or near-identical logic with only minor variations)
  appears in multiple places, extract it into a single shared function or module instead
  of copy-pasting or reimplementing it. Before writing new helper logic, search for
  an existing equivalent in shared/core packages and reuse it rather than writing
  a parallel implementation that can...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 70970
---

When the same logic (or near-identical logic with only minor variations) appears in multiple places, extract it into a single shared function or module instead of copy-pasting or reimplementing it. Before writing new helper logic, search for an existing equivalent in shared/core packages and reuse it rather than writing a parallel implementation that can drift out of sync.

Apply this in two directions:
1. Within a file/class: if several methods perform the same sequence of steps (e.g., setting flags, emitting an event, logging telemetry) with only the final shape differing, factor the common steps into one helper and let each caller supply just the differing piece.
2. Across the codebase: if a capability already exists in a shared or core package (e.g., shell-kind detection, git remote normalization, git preflight checks), import and reuse it instead of re-implementing it in an app-level file. When new logic needs to be shared between multiple apps, place it in the core/shared package it belongs next to (respecting the dependency direction: apps may depend on core, but core must never depend on an app), rather than leaving a second, divergent copy in the app.

Example — three methods each manually moved discarded items from a queue, built an event payload, and recorded telemetry:
```ts
// Before: repeated in shutdownSession, releaseSessionRuntime, and a third caller
const discarded = queue.splice(0);
emitEvent("pending_prompts", { discarded });
telemetry.record("prompts_discarded", discarded.length);

// After: one shared helper, each caller only supplies the entries and reason
private reportDiscardedPrompts(session, entries, reason) {
  this.emitEvent("pending_prompts", { discarded: entries });
  this.telemetry.record("prompts_discarded", entries.length);
}
```

Similarly, prefer `getShellKind()` from `@cline/shared` over a locally defined `isPowerShellCommand()`, and reuse `normalizeGitHubRemoteUrl` / existing git-preflight utilities instead of writing a second git runner. Consolidating duplicate logic keeps behavior consistent, shrinks the diff, and makes future changes a one-place edit instead of a multi-file hunt.</description>
