---
title: Avoid duplicated logic
description: When the same logic (HTTP calls, header construction, token/response
  parsing, or a derived value like a finish reason) appears in more than one place—whether
  across files or in separate branches of the same function—extract it into a single
  shared helper or service method and call it from both sites instead of copy-pasting.
  Duplicated code drifts over time:...
repository: decolua/9router?x
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31748
---

When the same logic (HTTP calls, header construction, token/response parsing, or a derived value like a finish reason) appears in more than one place—whether across files or in separate branches of the same function—extract it into a single shared helper or service method and call it from both sites instead of copy-pasting. Duplicated code drifts over time: a fix applied to one copy is easily missed in the other, leading to inconsistent behavior.

For example, instead of `ZedExecutor.refreshCredentials()` and `refreshZedToken()` independently re-implementing the same POST request, auth header format, and token-unwrapping logic, extract that into a shared `ZedService.refreshLlmToken()` and have both call it. Likewise, if two branches in `openaiResponsesToOpenAIResponse()` compute the same `finish_reason` logic, factor it into a small helper such as `computeFinishReason(state)` so there is one source of truth, and add a short comment when the logic relies on non-obvious sticky state.

Also keep function signatures honest: don't add parameters or options (e.g., an `onProgress` callback) that aren't actually wired up or used yet. Only introduce them once the functionality behind them is implemented, to avoid dead placeholders in the API surface.