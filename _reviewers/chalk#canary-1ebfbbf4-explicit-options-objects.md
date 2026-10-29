---
title: Explicit options objects
description: When a constructor or function accepts configuration, require an explicit,
  named options object rather than positional primitives (e.g. booleans). This keeps
  call sites self-documenting and leaves room to add new options without breaking
  existing call signatures.
repository: chalk/chalk#CANARY-1ebfbbf4
label: API
language: JavaScript
comments_count: 3
repository_stars: 23342
---

When a constructor or function accepts configuration, require an explicit, named options object rather than positional primitives (e.g. booleans). This keeps call sites self-documenting and leaves room to add new options without breaking existing call signatures.

Prefer:
```js
var ctx = new Chalk({enabled: false});
```
over:
```js
var ctx = new Chalk(false); // what does "false" configure?
```

When an options object can contain multiple properties that represent overlapping or derived state (e.g. a legacy `enabled` boolean alongside a newer `level` value), don't silently guess which one wins. Validate the combination up front and throw a clear, well-documented error if the values conflict:

```js
if ('enabled' in options && 'level' in options &&
    Boolean(options.level) !== Boolean(options.enabled)) {
  throw new Error('Invalid options; cannot have differing .level and .enabled values');
}
```

If one property is meant to be a convenience alias for another (as `enabled` is for `level`), implement it as a getter/setter that reads/writes the underlying canonical value, so both properties always stay in sync instead of duplicating state or logic. This avoids hairy branching logic, keeps backward-compatible options understandable, and makes the API's behavior predictable for consumers.</description>
</invoke>
