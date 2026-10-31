---
title: Extract shared logic
description: Avoid copy-pasting the same logic across files or across branches of
  the same function. When you find yourself writing nearly identical code in two places
  (e.g. the same HTTP call and response-unwrapping logic in two executors, the same
  JSON-repair routine imported into multiple translators, or the same finish-reason
  computation duplicated in a flush path...
repository: decolua/9router#zz237855c
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31752
---

Avoid copy-pasting the same logic across files or across branches of the same function. When you find yourself writing nearly identical code in two places (e.g. the same HTTP call and response-unwrapping logic in two executors, the same JSON-repair routine imported into multiple translators, or the same finish-reason computation duplicated in a flush path and a completion path), extract it into a single shared helper, service method, or module and have all call sites use it. This keeps the codebase DRY, ensures bug fixes and behavior changes propagate everywhere they're needed, and improves readability by giving the shared behavior one clear, well-named definition.

Example: instead of duplicating token-refresh logic in both `ZedExecutor.refreshCredentials()` and `refreshZedToken()`, extract it into `ZedService.refreshLlmToken()` and call that from both places. Similarly, instead of repeating finish-reason logic in two branches of `openaiResponsesToOpenAIResponse`, factor it into a `computeFinishReason(state)` helper used by both.

When extracting, place the shared code in an appropriately named concerns/utils module (as done with `toolArgs.js` for `repairDuplicatedJsonArguments`/`appendToolArgs`), and prefer composition/delegation over re-implementation. If the duplicated logic encodes non-obvious state or heuristics, add a brief comment explaining why the state is needed.