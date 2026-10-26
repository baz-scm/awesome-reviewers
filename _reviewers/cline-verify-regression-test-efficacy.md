---
title: Verify regression test efficacy
description: A test written for a bug fix is only useful if it actually distinguishes
  broken behavior from fixed behavior. Before merging, confirm each regression test
  fails against the pre-fix code and passes against the fix — don't just assert it
  "should" catch the bug.
repository: cline/cline
label: Testing
language: TypeScript
comments_count: 8
repository_stars: 70886
---

A test written for a bug fix is only useful if it actually distinguishes broken behavior from fixed behavior. Before merging, confirm each regression test fails against the pre-fix code and passes against the fix — don't just assert it "should" catch the bug.

This matters because it's easy to write a test that looks like it covers the fix but actually passes either way, giving false confidence. Examples of this failure mode: a test asserting on mocked resolved values without ever checking the pending/intermediate state that the fix actually changes (e.g. asserting a promise eventually resolves without first asserting it is *not yet* settled, so the test passes even against the buggy implementation that resolves too early or too late); a catalog-completeness test that strips away the exact signal (e.g. pluralization suffixes) it's supposed to validate, so a genuinely incomplete catalog still passes; or an assertion that only checks "no error thrown" instead of checking the specific symptom the bug caused.

When adding a test for a bug or edge case:
- Run it against the code before the fix and confirm it fails with the expected symptom.
- Run it against the fixed code and confirm it passes.
- If the test checks an intermediate/pending state (e.g. "not yet settled"), assert that state explicitly rather than only asserting the final outcome:

```ts
let settled = false
const invocation = doWork().finally(() => { settled = true })

await advanceTimersByTimeAsync(5_000)
expect(settled).toBe(false) // guards the "still waiting" behavior, not just the eventual result

// ...trigger completion...
await expect(invocation).resolves.toEqual(...)
```
- For fuzz/property-style tests, confirm the fuzzer or generator finds the bug on unfixed code and reports nothing on the fix.
- For cap/limit removals or data-shape invariants, add a test that fails if the old limit or shape is reintroduced, not just one that passes under the current state.

Treat "I verified this test fails without the fix" as a required step of the review, not an optional nice-to-have.