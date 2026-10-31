---
title: Extract shared logic
description: 'When the same logic appears in more than one place—whether in separate
  branches of a function or duplicated across multiple files/classes—extract it into
  a single shared helper, utility module, or service method instead of copy-pasting.
  Duplicated code drifts over time: a bug fix or behavior change applied to one copy
  is easily forgotten in the other,...'
repository: decolua/9router#pi240310
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31756
---

When the same logic appears in more than one place—whether in separate branches of a function or duplicated across multiple files/classes—extract it into a single shared helper, utility module, or service method instead of copy-pasting. Duplicated code drifts over time: a bug fix or behavior change applied to one copy is easily forgotten in the other, leading to inconsistent behavior.

Apply this rule at any scope:
- Within a function: if two branches compute the same result (e.g., a "finish reason" calculated independently in a flush path and a completed-response path), factor it into a dedicated function such as `computeFinishReason(state)` and call it from both places.
- Across files: if two modules implement the same parsing/repair/request logic (e.g., `repairDuplicatedJsonArguments`/`appendToolArgs` needed by both `openai-to-claude.js` and `kiro-to-claude.js`), move it into a shared module (e.g., `translator/concerns/toolArgs.js`) and import it from both.
- Across classes/services: if an executor and a token-refresh utility both implement the same HTTP call, auth-header construction, and response-unwrapping logic (e.g., Zed's LLM token refresh), consolidate that logic into one service method (e.g., `ZedService.refreshLlmToken()`) and have both callers delegate to it rather than reimplementing it.

Before adding a second implementation of existing logic, search for an existing helper/service to reuse or create one. When non-obvious state is used to drive shared logic (e.g., sticky flags), add a short comment explaining why, so future maintainers understand the intent when touching the shared code.</description>
</invoke>
