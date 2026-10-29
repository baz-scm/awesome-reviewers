---
title: Clear, fail-fast error messages
description: Distinguish between programmer errors and runtime/user-facing behavior
  changes when deciding how to handle failures, and make error messages easy to localize
  and act on.
repository: tj/commander.js
label: Error Handling
language: JavaScript
comments_count: 6
repository_stars: 28444
---

Distinguish between programmer errors and runtime/user-facing behavior changes when deciding how to handle failures, and make error messages easy to localize and act on.

- For invalid or misused API calls (e.g. bad argument syntax, duplicate command registration, invalid configuration), fail fast by throwing immediately with a clear, specific message rather than silently ignoring the problem or corrupting internal state. Example: throwing `passThroughOptions cannot be used for 'sub' without turning on enablePositionalOptions for parent command(s)` instead of silently continuing, or throwing when the same subcommand name is registered twice instead of letting it silently overwrite internals.
- For changes that affect existing end-user runtime behavior (not pure programmer misuse), prefer backward-compatible handling such as logging a warning or keeping old behavior rather than introducing a hard break, especially when the impact is ambiguous (e.g. detecting both `action` and `command:*` listeners registered, or detecting incompatible use of `.parse()` with async handlers). Only throw hard errors once the new behavior is well understood and justified.
- Build error messages compositionally instead of hardcoding natural-language words mixed with dynamic values, so messages remain translatable and consistent. Avoid baking words like "option" or "environment variable" directly into message templates; instead construct the full phrase (e.g. "option '--wrong'" or "'--wrong' (required environment variable: RIGHT)") as a single substitutable unit.
- Keep thrown messages focused: include only the context actually needed to diagnose and fix the issue (e.g. the failing command/option name), and avoid adding extra context that doesn't help resolution.

Example:
```js
// Fail fast on programmer misuse
if (parent && command._passThroughOptions && !parent._enablePositionalOptions) {
  throw new Error(`passThroughOptions cannot be used for '${command._name}' without turning on enablePositionalOptions for parent command(s)`);
}

// Prefer warning over breaking change for ambiguous behavior changes
if (isThenable(result) && !this._asyncParsing) {
  console.warn('Warning: .parse() used with an async handler; consider .parseAsync()');
}
```