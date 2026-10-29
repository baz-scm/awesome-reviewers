---
title: Hot-path efficiency
description: 'Code that runs per-request or in other hot paths must avoid unnecessary
  overhead. Prefer simple, cheap operations over heavier alternatives when both achieve
  the same result: use direct string checks instead of regex for trivial cases, use
  plain `for` loops instead of `Array#forEach`/closures in tight loops, and short-circuit
  work that isn''t needed (e.g....'
repository: Expressjs/Express
label: Performance Optimization
language: JavaScript
comments_count: 7
repository_stars: 69580
---

Code that runs per-request or in other hot paths must avoid unnecessary overhead. Prefer simple, cheap operations over heavier alternatives when both achieve the same result: use direct string checks instead of regex for trivial cases, use plain `for` loops instead of `Array#forEach`/closures in tight loops, and short-circuit work that isn't needed (e.g. skip calling a function when its input is empty). Never perform one-time setup work—such as `require()` calls, especially ones that may fail and therefore aren't cached—inside a function invoked on every request; move such setup to module load time instead. When introducing new code paths for performance reasons (e.g. streaming large payloads), favor native/streaming APIs appropriate to the data size, and back any performance-motivated design with benchmarks that reflect the actual production code paths and options being compared, not just the performance of an underlying dependency.

Example of moving a fragile require out of the hot path:
```js
// bad: require() runs on every call, and failures aren't cached
function send(chunk) {
  var WritableStream = require('stream/web').WritableStream; // may throw every time
  ...
}

// good: resolved once at module load
var WritableStream;
try {
  WritableStream = require('stream/web').WritableStream;
} catch (e) { /* not available */ }

function send(chunk) {
  if (WritableStream) { ... }
}
```