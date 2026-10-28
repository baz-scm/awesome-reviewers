---
title: Tests must prove the fix
description: A test for a bug fix or invariant must actually fail when the bug is
  reintroduced — writing it against the old (buggy) code first, or reverting the fix,
  is the fastest way to confirm this. Loose assertions (`toBeLessThan(naiveEstimate
  / 10)`, `.should` chains that silently pass on `undefined`, bounds like `eightSmallPlusOneHuge
  < oneSmallImage * 20`) can...
repository: cline/cline#|sleep 4
label: Testing
language: TypeScript
comments_count: 13
repository_stars: 70979
---

A test for a bug fix or invariant must actually fail when the bug is reintroduced — writing it against the old (buggy) code first, or reverting the fix, is the fastest way to confirm this. Loose assertions (`toBeLessThan(naiveEstimate / 10)`, `.should` chains that silently pass on `undefined`, bounds like `eightSmallPlusOneHuge < oneSmallImage * 20`) can pass even when the underlying logic is wrong; prefer exact-value or exact-behavior assertions instead (e.g. assert a flat per-item cost, or that payload size never moves an estimate at all, using fresh object instances when a cache keys by reference).

Where feasible, exercise the real code path rather than a mock that papers over the exact failure mode: run the actual SSH/shell script against a temp directory with symlinks, drive a provider through the real SDK adapter with a stubbed `fetch` instead of mocking the module, or boot the real compiled binary/entrypoint rather than asserting only `--version` works. When a cap, limit, or behavioral guarantee is removed or changed (e.g. "every failure persists for the session," "every plural catalog carries all required CLDR categories"), add a test that explicitly fails if the old limit is reintroduced, and keep assertions narrowly scoped to what is actually guaranteed (don't claim coverage, e.g. "independent of the catalog," that the test doesn't actually exercise).

For stateful or branching logic (UI state machines, retry/recovery matrices, verb sequences), cover the full relevant combination space with table-driven tests or targeted fuzzing over the invariants that must hold, in addition to the specific regression scenario. Balance this against proportionality: skip deep/brittle test scaffolding for low-risk, already-covered paths (e.g. a single log statement on a path with existing coverage), and prune redundant test cases that duplicate what another layer already owns.