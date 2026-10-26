---
title: Bound Complexity Pathologies
description: 'When implementing non-trivial algorithms, explicitly design for worst-case
  behavior and correctness under edge inputs.


  **Standards**

  - **Add explicit caps** for anything that can grow (archive bytes, number of files,
  recursion/link-follow depth, iteration counts). Fail fast with clear errors.'
repository: cline/cline#v7
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 70865
---

When implementing non-trivial algorithms, explicitly design for worst-case behavior and correctness under edge inputs.

**Standards**
- **Add explicit caps** for anything that can grow (archive bytes, number of files, recursion/link-follow depth, iteration counts). Fail fast with clear errors.
- **Avoid worst-case primitives**: prefer linear-time loops/parsers over regex patterns that can backtrack (or that are not provably linear).
- **Don’t scale costs with payload bytes when the model cost doesn’t**: compute estimates using the right unit (e.g., per-image) rather than naive char/base64 lengths.
- **Test pathological cases**: oversized inputs, deeply nested/looping structures, tricky separators/encodings—assert the output stays within expected bounds.

**Example (token estimation rule shape)**
```ts
const withoutImage = estimateRequestInputTokens({ messages: [{ role: 'user', content: [] }] });
const withSmall = estimateRequestInputTokens({
  messages: [{ role: 'user', content: [{ type: 'image', data: 'A', mediaType: 'image/png' }] }],
});
const withHuge = estimateRequestInputTokens({
  messages: [{ role: 'user', content: [{ type: 'image', data: 'A'.repeat(500_000), mediaType: 'image/png' }] }],
});

// payload size shouldn’t affect per-image billing
const perImage = withSmall - withoutImage;
console.assert(withHuge - withoutImage === perImage);
```

Adopting this prevents performance regressions and protects correctness when inputs are adversarial or simply large.