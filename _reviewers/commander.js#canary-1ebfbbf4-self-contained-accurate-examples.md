---
title: Self-contained, accurate examples
description: 'Documentation examples and guides must be complete, accurate, and unambiguous
  so a reader can use them without guessing or hitting errors. Specifically:'
repository: tj/commander.js#CANARY-1ebfbbf4
label: Documentation
language: Markdown
comments_count: 5
repository_stars: 28444
---

Documentation examples and guides must be complete, accurate, and unambiguous so a reader can use them without guessing or hitting errors. Specifically:

- Any helper function referenced in a code sample must either be defined inline in the doc, or its name must clearly signal that it's a placeholder the reader must implement (e.g. `myFindBestMatch` rather than an undefined `didYouMean`). Never leave a function "coming out of nowhere" that a first-time user might copy-paste and run into a `ReferenceError`.
- When documenting conventions or behavior (e.g. option/operand parsing order, POSIX vs. GNU rules), double-check the wording for technical correctness and give a concrete before/after example to remove ambiguity.
- When adding a new feature/option, update all related documentation in the same change: help text/usage examples, and add a worked example demonstrating both success and error cases.
- When documenting a pattern or caveat (e.g. optional-value options), ensure related variants (e.g. variadic options) are mentioned so the guidance is comprehensive and not misleading by omission.

Example — bad (undefined helper):
```js
program.on('command:*', (operands) => {
  console.error(`Did you mean '${didYouMean(operands[0])}'?`); // didYouMean is undefined
});
```

Example — good (clearly a placeholder, or implemented):
```js
const availableCommands = program.commands.map(cmd => cmd.name());
const suggestion = myFindBestMatch(operands[0], availableCommands); // reader implements this
console.error(`Did you mean '${suggestion}'?`);
```