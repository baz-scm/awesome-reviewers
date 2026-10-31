---
title: Eliminate duplicated logic
description: 'When the same logic (an HTTP call, a header format, a token-unwrapping
  routine, a finish-reason computation, etc.) appears in more than one place, extract
  it into a single, well-named helper or service method and have all call sites delegate
  to it. Duplicated logic tends to drift: a bug fix or behavior change applied to
  one copy is easily forgotten in the...'
repository: 'decolua/9router#

  exit 1'
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31737
---

When the same logic (an HTTP call, a header format, a token-unwrapping routine, a finish-reason computation, etc.) appears in more than one place, extract it into a single, well-named helper or service method and have all call sites delegate to it. Duplicated logic tends to drift: a bug fix or behavior change applied to one copy is easily forgotten in the other, leading to inconsistent behavior over time.

For example, instead of reimplementing the same `finish_reason` logic in both the flush path and the `response.completed` path:

```js
// Before: duplicated in two branches
if (!state.finishReasonSent && state.started) { /* compute reason A */ }
...
if (someOtherCondition) { /* compute reason B, nearly identical */ }

// After: single source of truth
function computeFinishReason(state) {
  return state.toolCallIndex > 0 || state.currentToolCallId ? "tool_calls" : "stop";
}
```

The same applies across files/modules: if `ZedExecutor.refreshCredentials()` and `refreshZedToken()` both post to `/client/llm_tokens`, build the same `Authorization` header, and unwrap the token the same way, move that shared behavior into one service method (e.g., `ZedService.refreshLlmToken()`) and have both call sites use it.

Additionally, keep function signatures and code free of dead weight: remove parameters, callbacks, or branches that aren't actually wired up or used yet (e.g., an `onProgress` parameter with no implementation), and add a short comment wherever logic relies on non-obvious or "sticky" state so future readers understand the intent without having to reverse-engineer it.