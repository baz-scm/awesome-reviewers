---
title: Branch-Exact Test Coverage
description: 'Make workflow/test suites “branch-complete and predicate-exact”: every
  reachable `case` arm and every required gating condition must be exercised and asserted,
  with environment-correct shims/guards.'
repository: QwenLM/qwen-code
label: Testing
language: JavaScript
comments_count: 12
repository_stars: 26407
---

Make workflow/test suites “branch-complete and predicate-exact”: every reachable `case` arm and every required gating condition must be exercised and asserted, with environment-correct shims/guards.

Apply this standard:
1) **Table-driven mapping tests must include every reachable branch** (don’t rely on bijection checks only over the listed subset). If a `case` arm exists in the implementation, it must appear in the ARMS/fixtures list.
2) **Ensure mocks/fixtures actually enter the new code path.** If the PR adds an `if`/mapping branch, add a test where that branch evaluates true (or explicitly covers each comparison outcome).
3) **Assert the full predicate, not just a prefix.** If the gate is `A && B && C`, your test should check that the produced script/body contains all three conditions (missing one enables false-green).
4) **Add OS/CI guards for end-to-end tests that rely on POSIX behavior or GNU tools.** Use `itOnUnix` or darwin-only shims for `sed -i` and avoid shebang/shim issues on Windows merge-queue.
5) **For timing/loop bugs, construct inputs so the code reaches the failing region** (e.g., ensure a retry loop re-enters after the deadline check).

Example patterns:
- **Include missing `case` arms in ARMS**
```js
const ARMS = [
  // ...existing arms...
  [{ VERDICT: 'infra-error' }, 'infra-error (crash, OOM, or unwritable results)', '基础设施故障（崩溃、OOM 或结果不可写）'],
  [{ VERDICT: '' }, 'unknown', '未知'],
];
expect(seenZh.size).toBe(ARMS.length);
```
- **Platform guard for POSIX npm shims**
```js
const itOnUnix = process.platform === 'win32' ? it.skip : it;
itOnUnix('fails on real critical vulnerability', () => {
  // end-to-end with npm shim
});
```
- **Predicate-exact assertion**
```js
// gate must require ASSERT_LINE as well as REPORT
expect(publishStep).toMatch(/\[ "\$\{VERDICT:-\}" = 'pass' \] && \[ -n "\$REPORT" \] && \[ -n "\$ASSERT_LINE" \]/);
```

If you follow these rules, regressions like “missing untested arms,” “new branch never executed,” “gate predicate weakened,” and “POSIX-only shims failing on Windows/macOS” are far less likely to slip through CI.