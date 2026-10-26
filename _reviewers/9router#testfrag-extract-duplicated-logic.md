---
title: Extract duplicated logic
description: When the same logic (parsing, HTTP calls, header construction, token
  unwrapping, or computed values like finish-reason) appears in more than one place—whether
  across different files or in separate branches of the same function—extract it into
  a single shared helper function or module instead of duplicating the implementation.
  Duplicated code increases the...
repository: decolua/9router#testfrag
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31419
---

When the same logic (parsing, HTTP calls, header construction, token unwrapping, or computed values like finish-reason) appears in more than one place—whether across different files or in separate branches of the same function—extract it into a single shared helper function or module instead of duplicating the implementation. Duplicated code increases the risk that a future bug fix or behavior change is applied in only one location, causing silent drift between the copies.

Apply this by:
- Identifying a canonical home for the shared logic (e.g., a `concerns/` utility module or an existing service class) and having all call sites import/delegate to it, rather than copy-pasting.
- When duplication occurs within a single function (e.g., identical logic computed in two conditional branches), factor it into a small named helper, e.g. `computeFinishReason(state)`, and call it from both branches.
- Preferring delegation to an existing service over introducing a second implementation, e.g. `ZedExecutor.refreshCredentials()` should delegate to `ZedService.refreshLlmToken()` rather than reimplementing the HTTP call and token-unwrap logic inline.

Example refactor:
```js
// Before: duplicated in two files
function sanitizeToolArgs(toolName, argsJson) {
  const repaired = repairDuplicatedJsonArguments(argsJson); // defined locally
  ...
}

// After: shared module
// open-sse/translator/concerns/toolArgs.js
export function repairDuplicatedJsonArguments(raw) { ... }
export function appendToolArgs(...) { ... }

// openai-to-claude.js & kiro-to-claude.js
import { repairDuplicatedJsonArguments } from "../concerns/toolArgs.js";
```

This keeps behavior consistent, reduces maintenance burden, and improves readability by giving the shared logic one clear, well-named location.