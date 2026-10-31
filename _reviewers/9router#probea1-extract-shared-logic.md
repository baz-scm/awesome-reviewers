---
title: Extract shared logic
description: 'When the same logic appears in more than one place — identical HTTP
  calls, header construction, token-unwrapping, parsing/repair routines, or branching
  logic like finish-reason computation — extract it into a single named helper function
  or shared module instead of copy-pasting it across files or branches. Duplicated
  implementations drift apart over time: a...'
repository: decolua/9router#probeA1
label: Code Style
language: JavaScript
comments_count: 4
repository_stars: 31730
---

When the same logic appears in more than one place — identical HTTP calls, header construction, token-unwrapping, parsing/repair routines, or branching logic like finish-reason computation — extract it into a single named helper function or shared module instead of copy-pasting it across files or branches. Duplicated implementations drift apart over time: a bug fix or edge-case patch applied to one copy is easily missed in the other, leading to inconsistent behavior.

Apply this by:
- Identifying near-identical blocks (same request shape, same unwrap/parse logic, same computed value) and moving them into one function with a clear name, e.g. `computeFinishReason(state)` instead of repeating the same if/else in two branches of the same file.
- Exporting cross-file duplicates from a shared concerns/utils module and importing it everywhere it's needed, e.g. moving `repairDuplicatedJsonArguments`/`appendToolArgs` into `translator/concerns/toolArgs.js` and importing from both `openai-to-claude.js` and `kiro-to-claude.js`, or consolidating the Zed token-refresh HTTP call + header format + response unwrapping into a single `ZedService.refreshLlmToken()` used by both `ZedExecutor.refreshCredentials()` and `tokenRefresh/providers.js`.
- Keeping function signatures minimal: don't add parameters (e.g. unused callbacks like `{ onProgress }`) until they are actually wired up and used, since unused surface area adds noise and false expectations for callers.
- Adding a short comment when the extracted logic relies on non-obvious state (e.g. sticky flags like `state.currentToolCallId`) so future readers understand why the branch exists.

This keeps behavior consistent across call sites, reduces the surface area reviewers need to re-check, and makes the codebase easier to read and maintain.