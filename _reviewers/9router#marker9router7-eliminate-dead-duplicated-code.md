---
title: Eliminate dead, duplicated code
description: 'Keep code lean, explicit, and self-explanatory: 1) Don''t add parameters,
  callbacks, or branches that aren''t wired up yet — a function''s signature should
  reflect only what it actually does (e.g., drop an unused `{ onProgress }` option
  until it''s implemented). 2) When the same logic (e.g., computing a finish reason)
  appears in multiple branches, extract it...'
repository: decolua/9router#MARKER9ROUTER7
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31425
---

Keep code lean, explicit, and self-explanatory: 1) Don't add parameters, callbacks, or branches that aren't wired up yet — a function's signature should reflect only what it actually does (e.g., drop an unused `{ onProgress }` option until it's implemented). 2) When the same logic (e.g., computing a finish reason) appears in multiple branches, extract it into a shared helper function so the implementations can't drift apart over time. 3) Prefer explicit, unambiguous expressions over relying on implicit type coercion — e.g., use `!!value` when a boolean is expected, rather than letting a truthy/falsy value leak through a logical `||`/`&&` chain. 4) When code depends on non-obvious state (such as "sticky" flags carried across calls), add a short comment explaining why, so future readers don't mistake it for a bug.

Example:
```js
// Bad: duplicated, implicit logic
function flush(state) {
  const reason = state.toolCallIndex > 0 || state.currentToolCallId ? "tool_calls" : "stop";
  ...
}
function onCompleted(state) {
  const reason = state.toolCallIndex > 0 || state.currentToolCallId ? "tool_calls" : "stop";
  ...
}

// Good: extracted helper, explicit boolean, documented intent
// `currentToolCallId` is sticky across chunks so late tool-call
// deltas still resolve to "tool_calls" even after the index resets.
function computeFinishReason(state) {
  return state.toolCallIndex > 0 || state.currentToolCallId ? "tool_calls" : "stop";
}

const hasThinkingMode = !!result.reasoning_effort || result.thinking?.type === "enabled";
```