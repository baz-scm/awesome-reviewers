---
title: Assertions must catch regressions
description: 'A test only earns its place if it actually fails when the behavior it
  claims to cover breaks. Several reviews found tests that looked thorough but would
  pass even with a broken implementation: an assertion like `value.should.deepEqual(...)`
  short-circuits on `undefined` instead of failing (use `should(value).deepEqual(...)`);
  fixtures that bundled multiple...'
repository: cline/cline;
label: Testing
language: TypeScript
comments_count: 11
repository_stars: 70964
---

A test only earns its place if it actually fails when the behavior it claims to cover breaks. Several reviews found tests that looked thorough but would pass even with a broken implementation: an assertion like `value.should.deepEqual(...)` short-circuits on `undefined` instead of failing (use `should(value).deepEqual(...)`); fixtures that bundled multiple signals together (e.g. every "overloaded" test case also had the word "overloaded" in its message) left one code path completely uncovered; and loose bounds-checks (`toBeLessThan(naive / 10)`) passed even though the real behavior should be an exact, payload-independent constant (`expect(estimate("A".repeat(500_000))).toBe(estimate("A"))`). The same risk shows up when mocking replaces the exact boundary being tested: round-tripping through a stub converter, or driving a provider through a fully mocked SDK, can hide bugs that only appear on the real wire format or the real adapter (e.g. the OpenAI transcription cast, the Cline provider headers on `doStream`, the SSH listing script run against a real temp directory with symlinks). Guard against this by: (1) isolating the one variable a case claims to test, with neutral values for everything else; (2) preferring exact/strict assertions over loose bounds when the real contract is exact; (3) exercising the real conversion/adapter/script path instead of a mock whenever the bug could live in that boundary; and (4) explicitly verifying the test's bite — temporarily reintroduce the bug (revert the fix, flip a flag, drop a header) and confirm the test fails. Treat "I checked it fails without the fix" as a required step, not an afterthought, for any test added to cover a bug.