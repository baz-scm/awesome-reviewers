---
title: Test regex alternations
description: When unit tests depend on filename/path classification via regex (e.g.,
  routing maintainers, detecting test files), add explicit test cases that exercise
  *every alternation token and mapping entry* in the regex/table. Uncovered alternations
  can fail silently if someone introduces a typo or refactors part of the pattern.
repository: QwenLM/qwen-code
label: Testing
language: Other
comments_count: 2
repository_stars: 26407
---

When unit tests depend on filename/path classification via regex (e.g., routing maintainers, detecting test files), add explicit test cases that exercise *every alternation token and mapping entry* in the regex/table. Uncovered alternations can fail silently if someone introduces a typo or refactors part of the pattern.

Apply this by:
- For each regex like `...|...|...`, create at least one `classify([...])` test per branch (e.g., `.test.`, `.spec.`, `__tests__`, `.test-utils.`).
- For each DOMAIN_MAP entry that uses alternation groups (e.g., `a|b|c`), add a test that targets a path matching that exact alternation.

Example (illustrative unit tests):
```js
it('treats .spec. as test-only', () => {
  const result = classify(['packages/core/src/tools/grep.spec.ts'], 'someone');
  assert.equal(result.reviewers.length, 0);
  assert.match(result.reason, /test-only/);
});

it('routes services compaction paths to the right domain expert', () => {
  const result = classify(['packages/core/src/services/compactionService.ts'], 'someone');
  assert.ok(result.reviewers.includes('LaZzyMan'));
});
```