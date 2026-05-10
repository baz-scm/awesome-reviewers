---
title: Comprehensive Test Coverage
description: When implementing or extending functionality, ensure tests (primarily
  unit tests for non-renderer code) cover the full supported behavior surface—not
  just a subset.
repository: mermaid-js/mermaid
label: Testing
language: Markdown
comments_count: 2
repository_stars: 87952
---

When implementing or extending functionality, ensure tests (primarily unit tests for non-renderer code) cover the full supported behavior surface—not just a subset.

Apply this as:
- For new/expanded supported inputs (e.g., HTML tags), add test cases for every supported variant.
- Keep unit tests mandatory for all non-renderer code; use integration tests for renderers.

Example pattern (unit-test style):
```js
const supportedTags = ['em','strong','sup','a','ul','li'];

describe('timeline label HTML support', () => {
  supportedTags.forEach((tag) => {
    it(`renders timeline label with <${tag}>`, () => {
      const input = `Label with <${tag}>text</${tag}>`;
      const output = renderTimelineLabel(input); // your unit-level function
      expect(output).toContainTag(tag); // adapt to your assertion style
    });
  });
});
```

This standard prevents partial coverage (only testing `<br>`/`<strong>`) and ensures consistent test expectations across the codebase.