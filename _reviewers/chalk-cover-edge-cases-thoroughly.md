---
title: Cover edge cases thoroughly
description: 'When writing or reviewing tests for new behavior, don''t stop at the
  happy path—actively think about edge cases, variations, and subtle state-sharing
  bugs that a naive fix could miss. Specifically: test both default/shared instances
  and custom instances (e.g. both `chalk` and `new chalk.Instance(...)`); add explicit
  tests for escaping/special-character...'
repository: chalk/chalk
label: Testing
language: JavaScript
comments_count: 4
repository_stars: 23342
---

When writing or reviewing tests for new behavior, don't stop at the happy path—actively think about edge cases, variations, and subtle state-sharing bugs that a naive fix could miss. Specifically: test both default/shared instances and custom instances (e.g. both `chalk` and `new chalk.Instance(...)`); add explicit tests for escaping/special-character handling whenever a function transforms or sanitizes input; and when testing caching or memoization, verify independence across combinations that share a sub-piece of state, not just across fully distinct styles. For example, testing `chalk.red.bold` vs `chalk.blue.bold` catches bugs where an internal `_styles` array is shared globally instead of per-instance, which a simpler test like `chalk.red('foo') !== chalk.blue('foo')` would not catch:

```js
const redBold = chalk.red.bold;
const blueBold = chalk.blue.bold;
assert.notEqual(blueBold('foo'), redBold('foo'));
```

Additionally, keep test fixtures and mocks deterministic and maintainable: prefer explicitly spoofing a dependency's exports (e.g. mocking `supports-color`) over relying on side-effecting environment flags whose behavior may change, and extract repeated setup logic (such as `__dirname`-based mocking) into a shared helper to avoid duplication across test files. Before marking a review comment resolved, double-check that the requested test was actually added.