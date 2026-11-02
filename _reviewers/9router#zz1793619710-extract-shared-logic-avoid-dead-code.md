---
title: Extract shared logic, avoid dead code
description: When the same logic appears in multiple places—across files (e.g., duplicated
  `repairDuplicatedJsonArguments`/`appendToolArgs` in two translator modules) or across
  branches within the same function (e.g., duplicated finish-reason computation in
  flush vs. response.completed paths)—extract it into a single shared helper function
  or module. This prevents the...
repository: decolua/9router#zz1793619710
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31855
---

When the same logic appears in multiple places—across files (e.g., duplicated `repairDuplicatedJsonArguments`/`appendToolArgs` in two translator modules) or across branches within the same function (e.g., duplicated finish-reason computation in flush vs. response.completed paths)—extract it into a single shared helper function or module. This prevents the implementations from drifting apart as one copy is updated without the other. For example, move shared utilities into a common module (`concerns/toolArgs.js`) and import it everywhere needed, or factor duplicated branch logic into a named helper like `computeFinishReason(state)`.

Likewise, avoid adding parameters, options, or code paths that aren't actually wired up or used yet (e.g., an `onProgress` callback with no caller). Speculative, unused code adds cognitive overhead and signals functionality that doesn't exist; add it only when it's actually needed and exercised. If behavior depends on non-obvious state (such as sticky flags carried across calls), add a short comment explaining why, so future readers don't mistake it for an oversight.