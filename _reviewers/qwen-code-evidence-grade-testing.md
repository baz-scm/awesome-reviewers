---
title: Evidence-grade Testing
description: When adding or updating test/verification logic, treat the harness setup
  as part of the test and ensure the evidence is causally attributable and non-vacuous.
repository: QwenLM/qwen-code
label: Testing
language: Markdown
comments_count: 5
repository_stars: 26407
---

When adding or updating test/verification logic, treat the harness setup as part of the test and ensure the evidence is causally attributable and non-vacuous.

**Standard**
1. **Isolate the control variable (no hidden confounds):** If your A/B or control relies on shared artifacts like `node_modules`, document and enforce when that’s a clean control. If dependency inputs change (e.g., `package.json`/lockfiles), either run a dependency-aware control or explicitly record the confound.
2. **Prove the wiring really points to the intended code:** In monorepos, internal workspace dependencies may symlink into the wrong (e.g., PR/head) tree. Add a check that resolves the actual runtime targets (e.g., `realpath` of resolved modules) and gate pass/fail of the verification on that.
3. **Require non-vacuity for “prove the test matters” runs:** If you validate a new/changed test by reverting/mutating inputs, the run must (a) reach the setup, and (b) fail the **intended assertion** with an expected-versus-actual mismatch message. If the revert breaks import/compile/setup before the assertion, record it as **inconclusive**, not proof.
4. **Regression-test the harness invariants (the harness is production code):** Add unit tests that pin subtle logic in your automation (e.g., stage-marker matching uses `startswith`, and you filter by bot author). Also ensure ids are re-resolved at patch time when threads/comments may have mixed order.

**Example pattern (monorepo control isolation)**
```bash
# Run from the base worktree.
# 1) Resolve what the code under test actually loads.
REALPATH=$(node -p "require('fs').realpathSync(require.resolve('@qwen-code/qwen-code-core'))")

# 2) Assert it points into the base tree (pseudo-check).
case "$REALPATH" in
  *tmp/base-tree/*) echo "OK wiring: $REALPATH" ;;
  *) echo "FAIL: base control resolved to non-base code: $REALPATH" ; exit 1 ;;
esac
```

**Example pattern (non-vacuity rule)**
- If reverting a key source hunk for a new test does not reach the intended assertion and produce the expected mismatch failure message, mark the vacuity check **inconclusive** and use an interface-preserving mutation instead.

**Example pattern (harness regression tests)**
- Add structural/unit tests that verify your comment/stage matching uses `startswith` (not `contains`) and filters by bot login, so a future edit can’t silently reintroduce clobbering behavior.