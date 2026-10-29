---
title: Verify algorithmic edge cases
description: When implementing pattern-matching, parsing, or stateful transformation
  algorithms, explicitly verify correctness against the full specification and against
  edge cases such as boundary values and nested/overlapping scopes. For example, a
  regex matching Unicode escapes must allow the full spec-defined range (up to 6 hex
  digits, values ≤ 0x10FFFF), not just a...
repository: chalk/chalk#CANARY-1ebfbbf4
label: Algorithms
language: JavaScript
comments_count: 3
repository_stars: 23342
---

When implementing pattern-matching, parsing, or stateful transformation algorithms, explicitly verify correctness against the full specification and against edge cases such as boundary values and nested/overlapping scopes. For example, a regex matching Unicode escapes must allow the full spec-defined range (up to 6 hex digits, values ≤ 0x10FFFF), not just a convenient subset. Similarly, algorithms that track open/close state (e.g., nested ANSI color codes) must correctly handle cases where inner and outer scopes share identical close markers, since naively closing on the first match can prematurely terminate an outer scope. Add a code comment or test case documenting the tricky scenario and why the chosen approach handles it, so future maintainers understand the algorithm's edge-case behavior.

Additionally, choose data structures that match the algorithm's access pattern: use a `Map` instead of a plain object for dynamic key-value lookups, as it offers better performance guarantees and avoids pitfalls like prototype pollution or implicit key coercion.

```js
// Bad: limited to 4 hex digits, misses spec-allowed \u{1,5 digits}
const TEMPLATE_REGEX = /\\(u[a-f\d]{4}|x[a-f\d]{2}|.)/gi;

// Good: matches full Unicode escape spec, including \u{...} up to 0x10FFFF
const TEMPLATE_REGEX = /\\(u(?:[a-f\d]{4}|\{[a-f\d]{1,5}\})|x[a-f\d]{2}|.)/gi;

// Use Map for lookup tables instead of plain objects
const ESCAPES = new Map([
	['n', '\n'],
	['t', '\t']
]);
```</description>
