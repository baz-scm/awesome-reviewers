---
title: Avoid Drift Constants
description: When code relies on values or logic that can diverge from the rest of
  the system (CSS/layout, shared pagination sizes, status-to-UI rules, helper behavior),
  prefer a single source of truth.
repository: QwenLM/qwen-code
label: Code Style
language: TSX
comments_count: 7
repository_stars: 26407
---

When code relies on values or logic that can diverge from the rest of the system (CSS/layout, shared pagination sizes, status-to-UI rules, helper behavior), prefer a single source of truth.

Apply these rules:
- No magic numbers for behavior thresholds or pagination: reuse existing constants (e.g., `SESSION_LIST_PAGE_SIZE`).
- No JS hardcoded layout measurements that mirror CSS: read the real values from `getComputedStyle(...)` (including `gap`) instead of subtracting assumed pixels.
- No duplicated mapping logic: centralize repeated `taskStatus -> label/tone/icon` (use a config object) so adding a new status can’t mismatch UI parts.
- No duplicated helper logic: reuse shared helpers like `getString(...)` rather than inlining type checks that may drift.
- Keep layout responsibility with the shell/owning component: wrap custom slots (header/footer) in consistent container elements so hosts don’t need to add ad-hoc margins.
- Delete unused exported UI components or ensure they’re actually used (avoid orphan files).

Example (centralized status mapping + constants):
```ts
const TASK_STATUS_CONFIG = {
  completed: { labelKey: 'system.taskCompleted', tone: 'success', Icon: CircleCheckIcon },
  failed: { labelKey: 'system.taskFailed', tone: 'error', Icon: CircleXIcon },
  cancelled: { labelKey: 'system.taskCancelled', tone: 'neutral', Icon: CircleMinusIcon },
} as const;

const statusConfig =
  (taskStatus && TASK_STATUS_CONFIG[taskStatus as keyof typeof TASK_STATUS_CONFIG]) ??
  { labelKey: 'system.taskNotification', tone: 'neutral', Icon: InfoIcon };

const page = await workspace.client.listWorkspaceSessions(cwd, {
  pageSize: SESSION_LIST_PAGE_SIZE,
});

const style = getComputedStyle(header);
const headerGap = parseFloat(style.gap) || 0;
```
This reduces silent UI breakage when constants, CSS, or helper behavior change over time.