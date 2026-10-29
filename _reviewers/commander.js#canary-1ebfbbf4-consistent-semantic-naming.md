---
title: Consistent semantic naming
description: Names for methods, properties, and tests must accurately reflect what
  they do and follow the conventions already established in the codebase, so readers
  can infer behavior without reading the implementation.
repository: tj/commander.js#CANARY-1ebfbbf4
label: Naming Conventions
language: JavaScript
comments_count: 8
repository_stars: 28444
---

Names for methods, properties, and tests must accurately reflect what they do and follow the conventions already established in the codebase, so readers can infer behavior without reading the implementation.

- Private members: prefix with an underscore (e.g. `_excessArguments`), and rename any new private helper/property to match (e.g. internal `opts` became `_options` to avoid clashing with the public `opts()` API).
- Verb/prefix families: when adding a new validation/check routine, follow the existing family naming pattern rather than inventing a new one. E.g. use `_checkForX` (matching `_checkForMissingMandatoryOptions`, `_checkForConflictingOptions`) instead of `_throwForX` when the routine doesn't always throw.
- Avoid misleading verbs: a name like `getCheckedArguments()` implies the caller uses the return value — don't use "get" if the result is sometimes discarded; prefer a name describing the side effect/check actually performed, or split the function so the name matches a single clear responsibility.
- Keep names scoped to a single concern: if a function bundles two unrelated behaviors (e.g. checking for unknown options and processing arguments), either split it into two clearly named functions or choose a name that honestly covers both, rather than a name that only reflects one of them.
- Public API renames (e.g. `unknownOption` → `unknownOptions` when the parameter becomes an array) are still subject to normal naming rules, but must be deferred to a major version if they are breaking changes.
- Test names should follow a `when <setup> then <expected result>` structure, e.g. `'when default value is object with custom toString then custom string displays in helpInformation'`.

Example:
```js
// Bad: implies it always throws, and doesn't match existing _checkForX family
_throwForMissingExecutable(file, dir, name) { ... }

// Good: matches existing naming family and actual behavior
_checkForMissingExecutable(file, dir, name) { ... }
```

Before merging a new or renamed identifier, check for an existing naming family/prefix convention and confirm the name matches the actual behavior (including visibility, side effects, and return usage).</description>
</RawReviewerOutputSchema>
