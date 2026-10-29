---
title: Extract shared logic
description: 'When the same logic (HTTP calls, header construction, parsing/repair
  routines, state-derived calculations, etc.) appears in more than one place, extract
  it into a single shared function or module and have all call sites use it, rather
  than letting near-identical implementations drift apart. Duplicated code is a maintenance
  hazard: a bug fix or behavior...'
repository: decolua/9router#%0Ainjected_key%3A%20pwned
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31638
---

When the same logic (HTTP calls, header construction, parsing/repair routines, state-derived calculations, etc.) appears in more than one place, extract it into a single shared function or module and have all call sites use it, rather than letting near-identical implementations drift apart. Duplicated code is a maintenance hazard: a bug fix or behavior change applied to one copy can easily be forgotten in the other(s).

Apply this by:
- Identifying when two code paths implement the same algorithm (e.g., JSON-argument repair logic duplicated between `openai-to-claude.js` and `kiro-to-claude.js`, or token-refresh/unwrap logic duplicated between an executor class and a provider-refresh utility) and moving the shared implementation into a common module (e.g., `concerns/toolArgs.js`, a shared `*Service` class) that both sides import/call.
- Factoring out repeated branch logic within a single function into a small named helper (e.g., `computeFinishReason(state)` instead of duplicating finish-reason computation in both the "flush" and "response.completed" branches), which also improves readability and documents intent.
- Adding a brief comment when the extracted logic depends on subtle/sticky state, so future readers understand why the shared helper behaves as it does.

Example:
```js
// Shared helper, single source of truth
export function computeFinishReason(state) {
  return state.toolCallIndex > 0 || state.currentToolCallId ? "tool_calls" : "stop";
}

// Used identically in both the flush path and the completed-event path
const finishReason = computeFinishReason(state);
```