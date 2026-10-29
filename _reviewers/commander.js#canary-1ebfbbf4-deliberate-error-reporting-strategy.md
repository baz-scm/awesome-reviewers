---
title: Deliberate error reporting strategy
description: When code encounters invalid programmer input or an inconsistent state,
  decide explicitly whether to throw, warn, or silently continue, and document the
  reasoning. Prefer throwing a clear error for invalid configuration or misuse (e.g.
  duplicate command registration, malformed argument definitions) so bugs surface
  early, rather than silently ignoring the...
repository: tj/commander.js#CANARY-1ebfbbf4
label: Error Handling
language: JavaScript
comments_count: 7
repository_stars: 28444
---

When code encounters invalid programmer input or an inconsistent state, decide explicitly whether to throw, warn, or silently continue, and document the reasoning. Prefer throwing a clear error for invalid configuration or misuse (e.g. duplicate command registration, malformed argument definitions) so bugs surface early, rather than silently ignoring the problem. However, when changing existing behavior could break code that previously worked without error, favor a non-breaking warning (and/or setting a signal like `process.exitCode`) over a hard throw, so existing consumers are alerted without being abruptly broken.

Whichever path is chosen, make sure the error message itself is correct and useful:
- Double-check the logic building the message (e.g. don't compare received values against argument names when you meant to just list the values).
- Include only the context that helps the developer act on the error (e.g. the current command name), and leave out details that add noise without adding value (e.g. parent command name in a nested error).
- Avoid hardcoding words like "option" or "environment variable" directly into the message template when the message may be translated/localized; keep such labels in substitutable parts so translators can control word order and terminology, e.g.:
```js
// Avoid:
return `option '${bestOption.flags}'`;

// Prefer: build the label as part of the interpolated value so the
// surrounding sentence/template can be fully localized.
```

Example of fail-fast vs graceful degradation tradeoff:
```js
// Fail fast on invalid programmer input
if (!argDetails) {
  throw new Error(`invalid argument definition: '${arg}'`);
}

// Graceful degradation when behavior change could break existing callers
if (isThenable(chain) && !this._asyncParsing) {
  chain.then(x => x, () => {}); // avoid unhandled rejection
  process.exitCode = 1; // signal an issue without hard-breaking the caller
  console.error('.parse() is incompatible with async argParsers, hooks and actions. Use .parseAsync() instead.');
}
```