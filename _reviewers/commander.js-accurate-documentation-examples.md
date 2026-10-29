---
title: Accurate documentation examples
description: 'Code examples in documentation must be technically correct, complete,
  and non-misleading. Before merging a doc change:


  - Verify any new behavior shown in an example is reflected everywhere it affects
  the docs (e.g., if you add an option, update the corresponding help-text example
  too), and add an example that demonstrates the resulting behavior (including...'
repository: tj/commander.js
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 28444
---

Code examples in documentation must be technically correct, complete, and non-misleading. Before merging a doc change:

- Verify any new behavior shown in an example is reflected everywhere it affects the docs (e.g., if you add an option, update the corresponding help-text example too), and add an example that demonstrates the resulting behavior (including error cases) so readers see the full picture.
- Double-check factual/technical claims in the prose (naming conventions, ordering rules, etc.) against the actual implementation or spec before publishing; don't rely on intuition if the behavior is nuanced (e.g., POSIX vs. GNU option/operand ordering).
- If an example relies on a function the user is expected to implement themselves (not provided by the library), name it in an obviously placeholder way (e.g., `myFindBestMatch` instead of `didYouMean`) or add a comment explaining it must be implemented, so a first-time user copying the snippet doesn't get a confusing "not defined" error.

Example of a misleading snippet to avoid:
```js
// BAD: didYouMean looks like a real API but isn't provided by the library
program.on('command:*', function (operands) {
  console.error(`Did you mean '${didYouMean(operands[0])}'?`);
});
```
```js
// GOOD: name clearly signals it's something the user must implement
const suggestion = myFindBestMatch(operands[0], availableCommands);
console.error(`Did you mean '${suggestion}'?`);
```