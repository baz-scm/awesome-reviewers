---
title: Contract-Driven Workflow Testing
description: 'Workflow logic changes can silently ship if tests don’t observe the
  exact contract your users/ops depend on. Adopt this checklist when writing/modifying
  tests around GitHub Actions scripts/workflows:'
repository: QwenLM/qwen-code
label: Testing
language: Yaml
comments_count: 8
repository_stars: 26407
---

Workflow logic changes can silently ship if tests don’t observe the exact contract your users/ops depend on. Adopt this checklist when writing/modifying tests around GitHub Actions scripts/workflows:

1) Assert the real user-visible contract
- If you change verdicts, headlines, or i18n formatting (emoji, <details><summary> text, interpolations), add assertions for the exact rendered strings—not just a loose substring.

2) Make stubs/fakes record critical invariants
- If behavior depends on argument values (e.g., retry budgets, timeouts, env vars), ensure your test harness stub captures and exposes those inputs.

3) Drive every critical branch with fixtures
- Ensure fixtures model non-empty upstream API responses so code paths like PATCH-vs-POST, fallback recovery, and “marker exists/doesn’t exist” are exercised. Don’t let comments/queries always return `[]` in fixtures if the production logic relies on that being sometimes non-empty.

4) Scope assertions to the correct job/step
- When helpers select steps by name, they may match the wrong job/step. Scope assertions through job selection (e.g., `job('verify')`) or step scoping (e.g., `stepIn(job, step)`) so the test proves the intended behavior.

Example pattern (branch + contract + invariant):
- Arrange: fixture returns an existing bot-owned “running” marker comment.
- Act: run the publisher with the stubbed API.
- Assert: it calls `PATCH /issues/comments/<id>` (not POST), and the new body contains the exact verdict headline.

This approach prevents the three common silent-failure modes shown in review: (a) tests only look at coarse substrings, (b) stubs discard the changed parameter so nothing is asserted, and (c) fixtures never reach the branch that would break in production.