---
title: Extract shared logic
description: 'When the same logic (HTTP calls, parsing/repair routines, response-state
  computations, etc.) appears in more than one file, pull it into a single shared
  helper or service module and have every call site import it, rather than copy-pasting
  the implementation. Duplicated code drifts over time: a bug fix or behavior change
  applied to one copy is easily...'
repository: 'decolua/9router#

  true'
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 31736
---

When the same logic (HTTP calls, parsing/repair routines, response-state computations, etc.) appears in more than one file, pull it into a single shared helper or service module and have every call site import it, rather than copy-pasting the implementation. Duplicated code drifts over time: a bug fix or behavior change applied to one copy is easily forgotten in the other, as seen with token-refresh logic repeated in both an executor and a provider helper, and with JSON-argument repair logic duplicated across two translators. Prefer a single source of truth: export the logic from a `concerns/` or `services/` module and import it wherever needed.

```js
// shared/concerns/toolArgs.js
export function repairDuplicatedJsonArguments(raw) { /* ... */ }

// openai-to-claude.js
import { repairDuplicatedJsonArguments } from "../concerns/toolArgs.js";

// kiro-to-claude.js
import { repairDuplicatedJsonArguments } from "../concerns/toolArgs.js";
```

This also applies to branching logic that computes the same value in multiple code paths (e.g., a `finish_reason` computed once in a "flush" branch and again in a "completed" branch) — extract it into a named helper such as `computeFinishReason(state)` so both paths stay in sync and the intent is documented in one place. When logic depends on non-obvious or "sticky" state, add a short comment explaining why, so future readers don't accidentally remove it during refactors.</description>
</invoke>
