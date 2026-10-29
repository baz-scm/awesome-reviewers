---
title: Validate boundaries and nesting
description: When writing parsing, looping, or stateful algorithms, explicitly verify
  behavior at boundary conditions and across the full valid input range rather than
  relying on a few manual test cases. For spec-driven logic (e.g. regex matching unicode
  escapes), check against the actual specification limits (such as max code point
  0x10FFFF, or 6-digit brace syntax)...
repository: chalk/chalk
label: Algorithms
language: JavaScript
comments_count: 4
repository_stars: 23342
---

When writing parsing, looping, or stateful algorithms, explicitly verify behavior at boundary conditions and across the full valid input range rather than relying on a few manual test cases. For spec-driven logic (e.g. regex matching unicode escapes), check against the actual specification limits (such as max code point 0x10FFFF, or 6-digit brace syntax) instead of assuming a fixed width. For loops that process a collection where one element was already consumed before the loop, double check the starting index to avoid off-by-one reprocessing (e.g. start at index 1 if index 0 was handled outside the loop). For algorithms that must preserve nested or recursive state (such as nested color-code wrapping), ensure the algorithm accounts for all occurrences of shared terminator/close tokens, not just the most recent one — otherwise nested state will incorrectly "leak" to an outer scope. Finally, pick data structures that match the access pattern and intent: use a `Map` instead of a plain object for dynamic key-value lookups, since it is both faster and semantically clearer as a container.

Example of correcting a boundary/spec issue:
```js
// Before: only matches 4-hex-digit unicode escapes
const TEMPLATE_REGEX = /\\(u[a-f\d]{4}|x[a-f\d]{2}|.)/gi;

// After: also matches brace syntax up to the spec-allowed max code point (0x10FFFF)
const TEMPLATE_REGEX = /\\(u(?:[a-f\d]{4}|\{[a-f\d]{1,5}\})|x[a-f\d]{2}|.)/gi;
```

Example of an off-by-one loop fix:
```js
var str = argsLen !== 0 && String(args[0]); // index 0 already consumed
for (var a = 1; a < argsLen; a++) { // start at 1, not 0
  str += ' ' + args[a];
}
```</description>
