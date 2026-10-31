---
title: Extract duplicated logic
description: When the same logic appears in more than one place—whether across separate
  files or as parallel branches within a single function—extract it into a single
  shared helper or module and have every call site use that one implementation. Duplicated
  code (e.g. identical HTTP calls and token-unwrap logic in two different executors,
  or repeated...
repository: decolua/9router#;sleep 4
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31756
---

When the same logic appears in more than one place—whether across separate files or as parallel branches within a single function—extract it into a single shared helper or module and have every call site use that one implementation. Duplicated code (e.g. identical HTTP calls and token-unwrap logic in two different executors, or repeated JSON-repair/argument-merging logic copied between translators, or finish-reason computation duplicated across two branches of the same function) is a maintenance hazard: a fix or behavior change applied to one copy silently fails to propagate to the other, producing hard-to-trace inconsistencies.

Before merging new code, check whether the logic you just wrote already exists elsewhere, and if so, factor it out:

```js
// Bad: same finish-reason logic duplicated in two branches
if (flushPath) {
  const finishReason = state.toolCallIndex > 0 ? "tool_calls" : "stop";
  ...
}
if (completedPath) {
  const finishReason = state.toolCallIndex > 0 ? "tool_calls" : "stop";
  ...
}

// Good: single shared helper used by both branches
function computeFinishReason(state) {
  return state.toolCallIndex > 0 || state.currentToolCallId ? "tool_calls" : "stop";
}
```

Similarly, shared request-building, parsing, or token-refresh logic should live in one concerns/service module (e.g. `toolArgs.js`, `ZedService.refreshLlmToken()`) and be imported by every consumer, rather than being copy-pasted per executor or translator.</description>
