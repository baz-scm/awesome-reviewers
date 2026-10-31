---
title: Extract shared logic
description: 'When the same logic appears in more than one place—whether in two separate
  files or two branches of the same function—extract it into a single shared helper
  or module rather than copy-pasting. Duplicated code (e.g., the same HTTP call and
  header format, the same JSON-repair routine, or the same finish-reason heuristic)
  tends to drift apart over time: a bug...'
repository: decolua/9router#`id -u`
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31732
---

When the same logic appears in more than one place—whether in two separate files or two branches of the same function—extract it into a single shared helper or module rather than copy-pasting. Duplicated code (e.g., the same HTTP call and header format, the same JSON-repair routine, or the same finish-reason heuristic) tends to drift apart over time: a bug fix or behavior change applied to one copy is easily forgotten in the other, leading to inconsistent behavior.

Apply this by:
- Identifying near-identical blocks of logic (parsing, request building, token unwrapping, state-derived calculations, etc.) across files or branches.
- Moving the common logic into a single exported function/module (e.g., a shared `toolArgs.js` concern, a `ZedService.refreshLlmToken()` method, or a `computeFinishReason(state)` helper) and having all call sites import/use it.
- Preferring delegation over re-implementation when two components need the same behavior, so future fixes only need to happen in one place.

Example:
```js
// Before: duplicated in two files
function sanitizeToolArgs(toolName, argsJson) { /* ...repair logic... */ }
// same repair logic copy-pasted in another translator file

// After: shared module
// open-sse/translator/concerns/toolArgs.js
export function repairDuplicatedJsonArguments(raw) { /* ... */ }
export function appendToolArgs(...) { /* ... */ }

// both openai-to-claude.js and kiro-to-claude.js import from toolArgs.js
```