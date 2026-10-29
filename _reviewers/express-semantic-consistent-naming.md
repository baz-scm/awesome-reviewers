---
title: Semantic, consistent naming
description: Choose names that clearly convey a variable's, function's, or module's
  purpose, type, and visibility, and keep that meaning consistent everywhere it's
  used. Follow established architectural naming patterns (e.g., name a use-case class
  `NotesService` rather than `NotesUseCase` if the codebase follows Controller-Service-Repository
  conventions). When requiring...
repository: Expressjs/Express
label: Naming Conventions
language: JavaScript
comments_count: 6
repository_stars: 69580
---

Choose names that clearly convey a variable's, function's, or module's purpose, type, and visibility, and keep that meaning consistent everywhere it's used. Follow established architectural naming patterns (e.g., name a use-case class `NotesService` rather than `NotesUseCase` if the codebase follows Controller-Service-Repository conventions). When requiring a module-specific identifier (such as a `deprecate` namespace), use the actual package name instead of an unrelated or component-specific string. Never repurpose the same property or variable name to mean different things in different contexts (e.g., don't reuse `_router` for both the public router proxy and an internal field with different semantics) — pick a distinct, descriptive name instead. For private or internal-only state, mark it clearly, e.g. with a leading underscore (`_router`, `_parsedQs`), so its intent is unambiguous. When dealing with function parameters, avoid reassigning the parameter itself (which can silently mutate `arguments` and trigger deopts); instead declare a new local variable with a related but distinct name, such as:

```js
function createApplication(options) {
  var opts = options || {};
  ...
}
```

Similarly, prefer a generic name like `val` over `obj` when a variable may hold any type, so the name doesn't mislead about the kind of value it stores. Consistent, intention-revealing names reduce confusion, prevent accidental misuse, and make code easier to review and maintain.