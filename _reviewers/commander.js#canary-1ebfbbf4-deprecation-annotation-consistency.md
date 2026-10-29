---
title: Deprecation annotation consistency
description: When marking APIs as deprecated, use a consistent `@deprecated` JSDoc
  format matching the rest of the codebase rather than introducing new styles (e.g.
  prefer `/** @deprecated since v8, instead use NewName */` over ad-hoc tags like
  `@linkcode`). Apply `@deprecated` annotations even to internal-only or private members
  if it gives useful IDE strikethrough...
repository: tj/commander.js#CANARY-1ebfbbf4
label: Documentation
language: TypeScript
comments_count: 3
repository_stars: 28444
---

When marking APIs as deprecated, use a consistent `@deprecated` JSDoc format matching the rest of the codebase rather than introducing new styles (e.g. prefer `/** @deprecated since v8, instead use NewName */` over ad-hoc tags like `@linkcode`). Apply `@deprecated` annotations even to internal-only or private members if it gives useful IDE strikethrough warnings to JavaScript consumers before the item is actually removed—this is especially valuable when `checkJs` is not enabled, since otherwise there is no other signal that the API is going away. At the same time, avoid redundant JSDoc annotations that duplicate information TypeScript already provides (e.g. `@param` type/name descriptions in `.d.ts` files); keep comments focused on information not already captured by the type system, such as deprecation notices, usage notes, or examples.