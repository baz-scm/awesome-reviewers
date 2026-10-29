---
title: Extract duplicated logic
description: Avoid duplicating logic across files or within multiple branches of the
  same function. When the same algorithm, HTTP call, parsing routine, or computation
  appears in more than one place, extract it into a single shared helper function
  or module and have all call sites use it. Duplicated code drifts over time—bug fixes
  and improvements applied to one copy...
repository: Decolua/9Router
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31641
---

Avoid duplicating logic across files or within multiple branches of the same function. When the same algorithm, HTTP call, parsing routine, or computation appears in more than one place, extract it into a single shared helper function or module and have all call sites use it. Duplicated code drifts over time—bug fixes and improvements applied to one copy are easily forgotten in the other(s), leading to inconsistent behavior.

Apply this whenever you notice:
- The same logic repeated in two files (e.g., identical JSON-repair or token-refresh code copied into two executors) — move it into a shared module (e.g., `concerns/toolArgs.js`, `ZedService.refreshLlmToken()`) and import it from both call sites.
- The same computation duplicated across branches within one function (e.g., finish-reason logic repeated in a flush path and a completion path) — factor it into a small named helper, such as `computeFinishReason(state)`, and call it from both branches.

Example refactor:
```js
// Before: duplicated in two branches
if (!state.finishReasonSent && state.started) {
  state.finishReasonSent = true;
  return { ...buildChunk(state), choices: [{ index: 0, delta: {}, finish_reason: "stop" }] };
}
// ...later, same pattern repeated for a different event...

// After: single source of truth
function computeFinishReason(state) {
  return state.toolCallIndex > 0 || state.currentToolCallId ? "tool_calls" : "stop";
}
```

When extracting shared logic that depends on non-obvious state (e.g., sticky flags like `state.currentToolCallId`), add a brief comment explaining why that state matters, so future maintainers understand the intent without re-deriving it.