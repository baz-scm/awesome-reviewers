---
title: Suppress output in CLI tests
description: When testing code paths that write to stderr/stdout or call process.exit
  (e.g. error handling, help, version output), avoid manually hijacking `process.exit`,
  `console.error`, or spying on `process.stderr.write`. These approaches are brittle,
  verbose, and pollute test output. Instead, use the library's built-in configuration
  hooks to suppress output and...
repository: tj/commander.js
label: Testing
language: JavaScript
comments_count: 3
repository_stars: 28444
---

When testing code paths that write to stderr/stdout or call process.exit (e.g. error handling, help, version output), avoid manually hijacking `process.exit`, `console.error`, or spying on `process.stderr.write`. These approaches are brittle, verbose, and pollute test output. Instead, use the library's built-in configuration hooks to suppress output and convert exits into catchable errors, and prefer shared test helpers/assertion utilities over ad-hoc mocks.

For example, instead of:
```js
var oldProcessExit = process.exit;
var oldConsoleError = console.error;
process.exit = function() { exceptionOccurred = true; throw new Error(); };
console.error = function() {};
```

use:
```js
const program = new commander.Command();
program
  .exitOverride()
  .configureOutput({ writeErr: () => {} });

assert.throws(
  () => program.parse(['node', 'test', '-m']),
  (err) => {
    assert.ok(err instanceof commander.CommanderError);
    assert.equal(err.exitCode, 1);
    assert.equal(err.code, 'commander.unknownOption');
    return true;
  },
);
```

Where many tests share this setup, factor it into a shared helper (e.g. `createTestCommand()`) so tests stay concise and consistent, and output-suppression logic isn't duplicated or forgotten. This keeps test output clean, makes assertions explicit and reliable, and avoids leaking global state changes (like reassigned `process.exit`) between tests.