---
title: Ensure CI-tested Workflows
description: All CI/CD-related script/workflow tests must be executed in CI, and they
  must assert the behaviors that matter in production—especially fail-closed security
  gates and correct step ordering.
repository: QwenLM/qwen-code
label: CI/CD
language: JavaScript
comments_count: 2
repository_stars: 26407
---

All CI/CD-related script/workflow tests must be executed in CI, and they must assert the behaviors that matter in production—especially fail-closed security gates and correct step ordering.

Apply it as a checklist:
1) **Wire tests into CI**: if you have `scripts/tests/*.test.js` (or `npm run test:scripts`), add a workflow step that runs it. Don’t rely on developers running tests locally.
2) **Test logic, not strings alone**: for security-sensitive workflow gating, include negative/deny scenarios and verify the intended allow/deny behavior (and any explanation/telemetry flags).
3) **Assert ordering, not just presence**: when workflow steps sweep/cleanup temporary dirs or delete symlinks, verify cleanup happens *after* any artifact staging/copying that must dereference symlinks, and before the final launch/upload step.

Example (ordering assertion pattern):
```js
const sweep = "find tmp -maxdepth 2 -type d -name '*-verify-*' -exec rm -rf {} +";
const stepText = getRunStepText(); // however your test builds/extracts it

const cpIndex = stepText.indexOf('cp -r');
const sweepIndex = stepText.indexOf(sweep);
expect(cpIndex).toBeGreaterThan(-1);
expect(sweepIndex).toBeGreaterThan(-1);
expect(cpIndex).toBeLessThan(sweepIndex); // fail if deletion moves earlier
```

This prevents regressions where CI wiring is missing and prevents “false green” tests where commands exist but run in the wrong order or weaken fail-closed gating.