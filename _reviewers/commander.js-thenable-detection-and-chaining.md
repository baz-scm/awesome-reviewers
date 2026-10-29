---
title: Thenable detection and chaining
description: When code must support both synchronous values and promises (e.g. user-supplied
  callbacks that may return a value or a Promise), detect "thenable" values by duck-typing
  (checking for a `.then` method) rather than using `instanceof Promise`. This is
  more robust and interoperable with any Promise-like implementation. Only perform
  async handling (await,...
repository: tj/commander.js
label: Concurrency
language: JavaScript
comments_count: 3
repository_stars: 28444
---

When code must support both synchronous values and promises (e.g. user-supplied callbacks that may return a value or a Promise), detect "thenable" values by duck-typing (checking for a `.then` method) rather than using `instanceof Promise`. This is more robust and interoperable with any Promise-like implementation. Only perform async handling (await, `.then`, wrapping) when the value is actually thenable; unconditionally awaiting or wrapping every value adds unnecessary tick delays and can mutate state (e.g. calling setters) for values that never needed async handling.

When chaining error handlers onto a thenable, make sure the result of `.catch()`/`.then()` is actually used (assigned or returned) — otherwise errors thrown inside the handler become unhandled rejections. Avoid attaching a `catch` handler to a promise that has already had its rejection handled upstream (e.g. inside a `.then()` callback), since this causes the error-refining logic to run twice. Prefer `promise.then(x => x, onRejected)` over `promise.catch(onRejected)` when you want to rely only on the `.then` method rather than the full Promise API, keeping the thenable contract minimal.

Example:
```js
function thenable(value) {
  return value && typeof value.then === 'function';
}

function handle(value, onError) {
  if (thenable(value)) {
    // Chain rejection handling once, using the result.
    return value.then(x => x, onError);
  }
  return value; // no unnecessary wrapping for plain values
}
```

Also, when normalizing a return value to a Promise (e.g. for consistent API behavior), you can often skip manual thenable checks altogether by relying on `Promise.resolve(value)`, which already handles both plain values and thenables correctly.