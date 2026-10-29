---
title: Extract duplicated logic
description: When the same logic is copy-pasted across files or repeated in multiple
  branches of the same function, factor it into a single shared helper or module instead
  of duplicating it. Duplicated code tends to drift — a fix applied to one copy is
  easily forgotten in the others — and it hurts readability. For example,...
repository: decolua/9router#MARKER9ROUTER7
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31644
---

When the same logic is copy-pasted across files or repeated in multiple branches of the same function, factor it into a single shared helper or module instead of duplicating it. Duplicated code tends to drift — a fix applied to one copy is easily forgotten in the others — and it hurts readability. For example, `repairDuplicatedJsonArguments`/`appendToolArgs` were duplicated across `openai-to-claude.js` and `kiro-to-claude.js`; they should live in (and were moved to) a shared module like `toolArgs.js` that both files import. Similarly, if finish-reason logic appears identically in two branches of a stream handler, extract it into a helper such as `computeFinishReason(state)` so there's one source of truth.

While organizing code, also avoid adding parameters or scaffolding that aren't used yet — e.g., don't add an `onProgress` callback to a function signature until the progress reporting is actually wired up; add it when it's needed, not preemptively. If logic depends on non-obvious state (such as "sticky" state carried across calls), add a brief comment explaining why, to keep the code self-documenting for future readers.