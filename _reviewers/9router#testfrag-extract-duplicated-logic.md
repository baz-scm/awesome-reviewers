---
title: Extract duplicated logic
description: 'When the same or near-identical logic appears in more than one place—whether
  in separate files, separate classes, or separate branches of the same function—extract
  it into a single shared helper, module, or service method rather than copy-pasting.
  Duplicated code drifts over time: a bug fix or behavior change applied to one copy
  is easily forgotten in the...'
repository: decolua/9router#testfrag
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31643
---

When the same or near-identical logic appears in more than one place—whether in separate files, separate classes, or separate branches of the same function—extract it into a single shared helper, module, or service method rather than copy-pasting. Duplicated code drifts over time: a bug fix or behavior change applied to one copy is easily forgotten in the other(s), leading to inconsistent behavior.

Apply this by:
1. Identifying repeated blocks (e.g., identical HTTP calls, same header construction, same parsing/unwrap logic, or the same computation performed in two code paths).
2. Moving the shared logic into a single function/module (e.g., a `concerns/` utility, a shared service method, or a small helper function) and having all call sites use it.
3. Naming the extracted helper clearly to convey intent (e.g., `computeFinishReason(state)` instead of inlining the same finish-reason calculation twice).

Example:
```js
// Before: same finish-reason logic duplicated in two branches
if (flushPath) {
  const finishReason = state.toolCallIndex > 0 ? "tool_calls" : "stop";
  ...
}
if (completedPath) {
  const finishReason = state.toolCallIndex > 0 ? "tool_calls" : "stop";
  ...
}

// After: single source of truth
function computeFinishReason(state) {
  return state.toolCallIndex > 0 || state.currentToolCallId ? "tool_calls" : "stop";
}
```

This keeps the codebase consistent, easier to review, and ensures fixes automatically apply everywhere the logic is used.</description>
</invoke>
