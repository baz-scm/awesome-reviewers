---
title: Tests must catch real bugs
description: 'A test is only as good as its ability to fail when the code is wrong.
  Before trusting a new test, check that it would actually catch the defect it claims
  to guard against:'
repository: "cline/cline\t"
label: Testing
language: TypeScript
comments_count: 7
repository_stars: 70947
---

A test is only as good as its ability to fail when the code is wrong. Before trusting a new test, check that it would actually catch the defect it claims to guard against:

- Avoid assertions that silently pass on missing data. Optional chaining before an assertion (e.g. `value?.should.deepEqual(...)`) short-circuits to a pass when `value` is `undefined`; use a form that fails instead (`should(value).deepEqual(...)`).
- Isolate the exact behavior under test. If every fixture shares a confounding signal (e.g. all "overloaded" error messages also contain the word "overloaded"), a check on one field (an error code) can pass for the wrong reason. Add fixtures that vary only the dimension being tested, with a neutral value for everything else.
- Assert the negative case explicitly, not just the positive one. If a feature is supposed to exclude/omit something, assert its absence (e.g. check an id is missing from a list), not just that the included case looks right — otherwise a regression that stops excluding anything goes unnoticed.
- Prefer exercising the real integration boundary over mocking it away. A test that only drives a mocked adapter or only checks a file exists on disk doesn't prove the real wiring (a live fetch call, a config loader, a type cast between library versions) works; add a case that goes through the real path with just the external edge (network, filesystem) stubbed.
- Stub at the correct layer. Don't hand a test double a resource that outlives the assertion (e.g. a never-ending stream) when stubbing a lower-level call would avoid leaking listeners/processes between tests.
- When in doubt, prove the test is meaningful: temporarily revert the fix (or mutate the implementation) and confirm the test fails; then confirm it passes again with the fix in place.