---
title: Consistent, semantic naming
description: Identifier and type names—especially those that are exported or otherwise
  semi-public—should be chosen deliberately and kept consistent across the codebase.
  Follow established conventions (e.g. `${Method}Options` for options types) and only
  deviate when there's a clear reason, since renaming an exported type or prop can
  be a breaking change for consumers...
repository: facebook/react#b20
label: Naming Conventions
language: JavaScript
comments_count: 4
repository_stars: 251895
---

Identifier and type names—especially those that are exported or otherwise semi-public—should be chosen deliberately and kept consistent across the codebase. Follow established conventions (e.g. `${Method}Options` for options types) and only deviate when there's a clear reason, since renaming an exported type or prop can be a breaking change for consumers (see how `RenderToReadableStreamOptions` had to match a name already assumed by DefinitelyTyped). When renaming an identifier, grep the whole repo to confirm every usage/fixture is updated; stale references (e.g. a typo'd prop name with a default fallback) can silently pass tests instead of failing.

Names should also be semantically accurate rather than generically convenient: prefer the most precise/common term users would expect (e.g. label an object as `Promise` rather than the more technically correct but less familiar `Thenable`, falling back to the generic term only when no better name is available). Suffixes like `Static` should only be added when needed to disambiguate from a similarly-named counterpart (e.g. a render-specific flag); don't apply a suffix pattern just for uniformity if there's nothing to disambiguate.

Example:
```js
// Good: name matches convention and is unambiguous
export type RenderToReadableStreamOptions = {...};

// Good: no suffix needed, nothing to disambiguate from
export const Forked = /* ... */ 0b00000000001...;

// Bad: unnecessary suffix when no counterpart exists
export const ForkedStatic = /* ... */ 0b00000000001...;
```
</description>
</invoke>
