---
title: API consistency with conventions
description: When adding new public API surface, follow the structural and naming
  conventions already established elsewhere in the API rather than introducing one-off
  patterns. This keeps the interface predictable and easy to learn.
repository: tj/commander.js#CANARY-1ebfbbf4
label: API
language: JavaScript
comments_count: 4
repository_stars: 28444
---

When adding new public API surface, follow the structural and naming conventions already established elsewhere in the API rather than introducing one-off patterns. This keeps the interface predictable and easy to learn.

Concretely:
- Collections of a typed concept should hold that type consistently. If `.commands` holds `Command` instances and `.options` holds `Option` instances, then `.args`/`_args` should hold `Argument` instances rather than plain objects, so callers can rely on a uniform shape across the API.
- If you introduce an extensibility pattern (e.g. a `createX()` factory to allow subclassing), apply it consistently across all equivalent concepts (`createCommand()`, `createOption()`, `createHelp()`, `createArgument()`) rather than special-casing some but not others.
- Design getters/setters symmetrically. For example, prefer a single array parameter for both getting and setting (`aliases(['a','b'])` / `aliases()`) rather than mixing varargs for the setter with an array-returning getter.
- Avoid naming collisions with existing properties/methods when adding related functionality (e.g. don't add a new `opts` property that overlaps semantically with an existing `options` array — pick a name and shape that clearly disambiguates the two).

Example — keep arrays strongly typed instead of exposing internal plain objects:
```js
// Avoid: pushes a loosely-typed internal detail
addArgument(argument) {
  this._args.push(argument.argDetails);
}

// Prefer: keep the public array consistent with other typed collections
addArgument(argument) {
  this._args.push(argument); // same pattern as this.commands.push(cmd) / this.options.push(option)
}
```

Before adding a new method, property, or event, check how similar concepts are already modeled in the API and mirror that shape, naming, and behavior. If a deviation is necessary, document why.