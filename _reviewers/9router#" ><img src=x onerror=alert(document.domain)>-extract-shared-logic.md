---
title: Extract shared logic
description: When the same logic appears in more than one place — whether across files
  or as repeated branches within a single function — extract it into a single, well-named
  helper function or shared module instead of copy-pasting. Duplicated logic (e.g.,
  identical JSON-repair helpers in two translator files, near-identical HTTP token-refresh
  code in an executor and a...
repository: decolua/9router#" ><img src=x onerror=alert(document.domain)>
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31680
---

When the same logic appears in more than one place — whether across files or as repeated branches within a single function — extract it into a single, well-named helper function or shared module instead of copy-pasting. Duplicated logic (e.g., identical JSON-repair helpers in two translator files, near-identical HTTP token-refresh code in an executor and a token-refresh service, or the same finish-reason computation repeated in two branches of a response handler) causes drift: a bug fix or improvement applied to one copy is easily forgotten in the other(s), and readers have to verify both copies are still in sync.

Apply this by:
- Moving duplicated utility functions into a shared `concerns/`, `utils/`, or `services/` module and importing it from every call site (e.g., `repairDuplicatedJsonArguments`/`appendToolArgs` moved to `open-sse/translator/concerns/toolArgs.js` and imported by both `openai-to-claude.js` and `kiro-to-claude.js`).
- When two components implement the same external call and response-unwrapping logic (e.g., Zed's token-refresh HTTP call and token unwrap present in both `ZedExecutor.refreshCredentials()` and `refreshZedToken()`), consolidate into one service method (e.g., `ZedService.refreshLlmToken()`) and have both callers delegate to it.
- When the same computation recurs across multiple branches of one function (e.g., finish-reason logic appearing both in a flush path and a `response.completed` path), factor it into a small helper like `computeFinishReason(state)` and call it from each branch.
- Add a short comment when the extracted logic relies on non-obvious or "sticky" state so future readers understand the intent without re-deriving it.

This keeps the codebase organized, reduces the surface area for inconsistent bug fixes, and makes intent clearer for future readers.