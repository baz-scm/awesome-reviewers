---
title: Accurate, convention-consistent naming
description: Names of methods, functions, and variables must precisely describe what
  the code actually does, and should follow the established naming conventions already
  used elsewhere in the codebase.
repository: tj/commander.js
label: Naming Conventions
language: JavaScript
comments_count: 6
repository_stars: 28444
---

Names of methods, functions, and variables must precisely describe what the code actually does, and should follow the established naming conventions already used elsewhere in the codebase.

- Avoid misleading verbs/nouns: don't call something `_throwForX` if it doesn't always throw, or `getX()` if the caller often ignores the return value. Pick a name that matches the real behavior, e.g. rename `_throwForMissingExecutable` to `_checkForMissingExecutable`.
- Reuse existing naming patterns for similar routines instead of inventing new ones. This codebase already has a family of `_checkForX` validators (`_checkForMissingMandatoryOptions`, `_checkForConflictingOptions`, `_checkForBrokenPassThrough`, etc.) — new validation methods should follow that same `_checkForX` pattern rather than ad-hoc names like `_checkForIllegalPassThroughOptions` (which was also semantically wrong, since "illegal" didn't capture that it's a broken *combination* of settings).
- Mark private/internal methods consistently, e.g. prefix with `_` as done for `_excessArguments`, so API surface is clear at a glance.
- Keep names grammatically consistent with the actual data shape (singular vs. plural): if a method's parameter changes from a single value to an array (e.g. `unknownOption(flag)` now receiving multiple unknown options), rename it to `unknownOptions` to reflect that — but if the method is public API, treat the rename as a breaking change and schedule it for the next major release rather than doing it silently.
- When a function's responsibilities change (e.g. a helper that used to just "preprocess" now also performs an unrelated check), either rename it to reflect its new combined behavior or split it back into focused functions whose names clearly match their single responsibility.

Example:
```js
// Bad: implies it always throws, doesn't match sibling naming
_throwForMissingExecutable(executableFile, executableDir, subcommandName) { ... }

// Good: follows existing _checkForX convention and reflects actual behavior
_checkForMissingExecutable(executableFile, executableDir, subcommandName) { ... }
```

Before merging, review method/variable names against their implementation and against similarly-purposed names already in the file to ensure clarity and consistency.</description>
</invoke>
