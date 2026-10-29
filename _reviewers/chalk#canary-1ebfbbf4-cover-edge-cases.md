---
title: Cover edge cases
description: When adding a test for new behavior, don't stop at the simplest case—extend
  coverage to nested/chained combinations, interactions between multiple instances,
  and edge-case inputs (e.g. special characters that need escaping). Minimal, isolated
  tests often pass while missing bugs that only surface under realistic or combined
  usage, such as shared-state issues...
repository: chalk/chalk#CANARY-1ebfbbf4
label: Testing
language: JavaScript
comments_count: 4
repository_stars: 23342
---

When adding a test for new behavior, don't stop at the simplest case—extend coverage to nested/chained combinations, interactions between multiple instances, and edge-case inputs (e.g. special characters that need escaping). Minimal, isolated tests often pass while missing bugs that only surface under realistic or combined usage, such as shared-state issues between cached style instances or incorrect handling of nested template substitutions.

For example, instead of only testing:
```js
assert.notEqual(chalk.red('foo'), chalk.blue('foo'));
```
also add a test that exercises combined/chained styles to catch subtler bugs:
```js
const redBold = chalk.red.bold;
const blueBold = chalk.blue.bold;
assert.notEqual(blueBold('foo'), redBold('foo'));
```
Similarly, when testing template-literal substitutions, verify deeper chains (e.g. `chalk.bold.red.underline\`Hello\``) and verify that special characters in interpolated arguments are properly escaped. Always ask: "What combined, nested, or edge-case scenario could break this feature even if the basic case works?" and add a corresponding test.