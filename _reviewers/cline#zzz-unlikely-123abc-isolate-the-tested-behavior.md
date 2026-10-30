---
title: Isolate the tested behavior
description: When writing a test (especially a regression test for a bug fix), design
  the fixture so it exercises only the specific mechanism being verified, not an incidental
  detail that could make the assertion pass for the wrong reason. A test that is accidentally
  confounded will not catch the next regression.
repository: cline/cline#zzz-unlikely-123abc
label: Testing
language: TypeScript
comments_count: 8
repository_stars: 71035
---

When writing a test (especially a regression test for a bug fix), design the fixture so it exercises only the specific mechanism being verified, not an incidental detail that could make the assertion pass for the wrong reason. A test that is accidentally confounded will not catch the next regression.

Concretely:
- Vary one dimension at a time. If a classifier keys off both a message and a code, write cases with a neutral message and a real code (and vice versa), not fixtures where both signals point the same way.
- Include adversarial/boundary values in parsed input: filenames with tabs, glob characters, or other delimiters the parser itself uses, not just "normal" names.
- When a flag or field has a precedence rule, test the case where multiple flags are present together, not just each one in isolation.
- Prefer exact/tight assertions over loose magnitude bounds when the underlying computation is meant to be deterministic or invariant. If a cost is supposed to be flat regardless of payload size, assert equality across a tiny and a huge payload, not just "less than some generous multiple."
- When a code path has two call sites that share logic but could diverge (e.g., streaming vs. non-streaming), cover both explicitly instead of assuming parity.
- For regression tests, reproduce the exact scenario that hid the original bug (e.g., the nested/edge-case shape that caused mis-routing), not just a simplified version of it.

Example, tightening a loose per-image cost assertion into one that actually pins the invariant:

```ts
it("charges a flat cost per image, independent of payload length", () => {
  const estimate = (data: string) =>
    estimateRequestInputTokens({
      messages: [{ role: "user", content: [{ type: "image", data, mediaType: "image/png" }] }],
    });

  // Equality, not "less than some generous bound" — size must not move the estimate at all.
  expect(estimate("A".repeat(500_000))).toBe(estimate("A"));
});
```

Applying this discipline turns a passing-by-coincidence test into one that will actually fail the next time the behavior regresses.