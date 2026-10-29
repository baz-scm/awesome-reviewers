---
title: Safe handling of thenable values
description: When code must support both synchronous and asynchronous (Promise-returning)
  values, detect "thenable" values with duck-typing (e.g. `typeof value.then === 'function'`)
  instead of `instanceof Promise`, since many promise-like objects do not pass an
  `instanceof` check. Only perform async operations (such as `await`, `.then()`, or
  wrapping in...
repository: tj/commander.js#CANARY-1ebfbbf4
label: Concurrency
language: JavaScript
comments_count: 4
repository_stars: 28444
---

When code must support both synchronous and asynchronous (Promise-returning) values, detect "thenable" values with duck-typing (e.g. `typeof value.then === 'function'`) instead of `instanceof Promise`, since many promise-like objects do not pass an `instanceof` check. Only perform async operations (such as `await`, `.then()`, or wrapping in `Promise.resolve`) when a value is actually thenable; forcing every value through `Promise.resolve` or `await` introduces an extra microtask tick and unwanted side effects for purely synchronous code paths, and scatters promise-handling logic across the codebase instead of centralizing it where the async boundary genuinely exists.

When chaining promise handling for error refinement or further processing, be careful not to create unhandled rejections or re-handle an already-handled error. If an error handler re-throws (e.g. `refineError`), assign the result of `.catch()`/`.then()` back to the variable being returned so the error propagates correctly, and attach error handling as part of the same chain (e.g. inside the `previous.then(...)` callback) rather than appending a second `.catch()` afterward, which could re-invoke the handler on an error that was already rethrown. Prefer `result.then(onFulfilled, onRejected)` over `result.catch(onRejected)` when you only need `.then` support, since this works for any thenable rather than only values with a `.catch` method.

Example:
```js
function isThenable(value) {
  return value && typeof value.then === 'function';
}

function parseArg(target, value, previous, invalidArgumentMessage) {
  const refineError = (err) => {
    // ...custom error handling, then rethrow
    throw err;
  };

  if (isThenable(previous)) {
    // Attach error handling inside the same chain, do not catch twice.
    return previous.then(
      (resolvedPrevious) => target.parseArg(value, resolvedPrevious),
      refineError
    );
  }

  try {
    return target.parseArg(value, previous);
  } catch (err) {
    refineError(err);
  }
}
```