---
title: No Console Logging
description: Avoid direct `console.log`/`console.warn` (and other `console.*`) in
  application code—especially in TUI/interactive flows—because it can break rendering
  and other runtime behavior. Route all log/diagnostic output through the project’s
  logging/UI abstraction so messages are formatted and displayed consistently.
repository: earendil-works/pi
label: Logging
language: TypeScript
comments_count: 2
repository_stars: 79783
---

Avoid direct `console.log`/`console.warn` (and other `console.*`) in application code—especially in TUI/interactive flows—because it can break rendering and other runtime behavior. Route all log/diagnostic output through the project’s logging/UI abstraction so messages are formatted and displayed consistently.

Apply this rule by:
- Replacing `console.*` calls with the existing notification/logging mechanism (e.g., `uiContext.notify(message, level)` or a centralized logger).
- Preserving log levels (`info`, `warn`, `error`) in the chosen API.
- Using the proper fallback path that still respects the UI/logging layer (not raw stdout/stderr).

Example (pattern):
```ts
// Bad (don’t do this)
console.warn("[pi-ai] Skipping unsigned thinking block");

// Good
uiContext.notify("Skipping unsigned thinking block", "warn");
```
If a function currently falls back to `console.log` when UI isn’t available, refactor it to use an injected logger (or a non-TUI-safe abstraction) instead of writing to the console directly.