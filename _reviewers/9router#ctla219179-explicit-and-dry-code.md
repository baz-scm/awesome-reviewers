---
title: Explicit and DRY code
description: 'Write code that says exactly what it does and avoid unnecessary repetition.
  Concretely:


  1. Remove unused parameters, options, or dead code paths. If a feature (e.g. a progress
  callback) isn''t actually wired up yet, don''t add a placeholder parameter for it
  — add it when it''s implemented.'
repository: decolua/9router#ctlA219179
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31730
---

Write code that says exactly what it does and avoid unnecessary repetition. Concretely:

1. Remove unused parameters, options, or dead code paths. If a feature (e.g. a progress callback) isn't actually wired up yet, don't add a placeholder parameter for it — add it when it's implemented.

2. Make type coercions explicit, especially for boolean checks built from values that may not be booleans (numbers, strings, undefined). Use `!!` or an equivalent explicit conversion so the resulting variable's type and intent are unambiguous:

```js
// Avoid - result may not be a real boolean
const hasThinkingMode = result.reasoning_effort || result.thinking?.type === "enabled";

// Prefer
const hasThinkingMode = !!result.reasoning_effort || result.thinking?.type === "enabled";
```

3. Avoid duplicating logic across branches (e.g. computing a "finish reason" in both a flush path and a completion-event path). Extract shared logic into a small, named helper function such as `computeFinishReason(state)` so future changes only need to happen in one place, and the intent is clear from the function name.

4. When logic depends on subtle or "sticky" state (flags that persist across calls, like `state.currentToolCallId`), add a short comment explaining why the state is checked that way, so future readers don't misinterpret the intent.

Applying these practices keeps code intention-revealing, reduces the chance of divergent logic during future edits, and prevents readers from being misled by vestigial parameters or implicit type coercions.</description>
</invoke>
