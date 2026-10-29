---
title: Consistent, backward-compatible API
description: When adding or changing public methods, properties, or events, make sure
  the new surface area is consistent with existing conventions and does not silently
  break current behavior.
repository: tj/commander.js
label: API
language: JavaScript
comments_count: 6
repository_stars: 28444
---

When adding or changing public methods, properties, or events, make sure the new surface area is consistent with existing conventions and does not silently break current behavior.

- Reuse established patterns instead of inventing new ones: if the library already supports a `createCommand()`/`createOption()` factory style for subclassing, add new extension points (e.g. `createArgument()`) the same way rather than asking callers to instantiate internal classes directly.
- Keep collections uniform: if `.commands` and `.options` already store class instances, new collections like `.args`/`_args` should also store the actual class instance (e.g. `Argument`), not plain objects, so callers can rely on a single, predictable shape.
- Preserve symmetry between getters and setters: prefer a single parameter type (e.g. an array) for both the getter and setter of a method such as `aliases()`, rather than mixing `arguments.length`-based varargs with array-based getters.
- Avoid naming collisions and unexpected side effects on existing state. Adding a new property or behavior should not shadow or clobber data a caller may already be using:
  ```js
  // Bad: introduces a new property that collides with intent of existing `options`
  this.options = [];
  this.opts = {}; // confusing overlap, breaks expectations of namespacing

  // Good: pick a name that doesn't conflict and clearly documents intent
  this.optsSnapshot = this.opts();
  ```
- When introducing new reserved flags, keywords, or automatic behaviors (e.g. special CLI flags for a new feature), guard them so they only activate when the feature is explicitly opted into (e.g. only parse special flags if the user has defined completion rules), to avoid breaking existing user code that already uses those names.
- Mutating one piece of state (e.g. setting a non-persistent option value) must not implicitly clear or alter unrelated state (e.g. a persistent value) unless that is the explicit, documented contract.

Before merging an API change, ask: "Does this match our existing patterns, could it collide with something a user already relies on, and does it have any non-obvious side effects on other state?" If yes to any, redesign before shipping.</description>
