---
title: Informative error messages
description: Error messages should be specific, actionable, and include context that
  helps developers understand and fix the issue. Use standard error codes that can
  be tested and suppressed rather than relying only on text messages. Create errors
  at the point of detection rather than inside callbacks to preserve useful stack
  traces.
repository: nodejs/node
label: Error Handling
language: JavaScript
comments_count: 8
repository_stars: 112178
---

Error messages should be specific, actionable, and include context that helps developers understand and fix the issue. Use standard error codes that can be tested and suppressed rather than relying only on text messages. Create errors at the point of detection rather than inside callbacks to preserve useful stack traces.

When creating custom error messages for complex scenarios, include:
1. What went wrong (the specific condition that failed)
2. Why it matters (the impact of the failure)
3. How to fix it (clear steps to resolve the issue)

Example of an improved error message:

```javascript
// Instead of:
throw new Error('Invalid module format');

// Prefer:
throw new ERR_AMBIGUOUS_MODULE_SYNTAX(
  'Cannot determine intended module format because both `require()` and top-level ' +
  '`await` are present. If the code is intended to be CommonJS, wrap `await` in an ' +
  'async function. If the code is intended to be an ES module, replace `require()` ' +
  'with `import`.'
);

// And when testing, check the code, not the message:
assert.throws(() => moduleOperation(), { code: 'ERR_AMBIGUOUS_MODULE_SYNTAX' });
```

For warnings that should be suppressible, always use a warning code:

```javascript
process.emitWarning(
  'Detected `fs.readFile()` to read a huge file in memory. Consider using ' +
  '`fs.createReadStream()` instead to minimize memory overhead.',
  'ERR_FS_FILE_TOO_LARGE'
);
```

When handling errors in async contexts, create the error object before entering the async callback to ensure it has a useful stack trace:

```javascript
// Instead of:
if (options.signal?.aborted) {
  return process.nextTick(() => callback(new AbortError()));
}

// Prefer:
if (options.signal?.aborted) {
  const err = new AbortError();
  return process.nextTick(() => callback(err));
}
```