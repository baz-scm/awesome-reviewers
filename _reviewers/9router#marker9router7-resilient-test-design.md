---
title: Resilient test design
description: 'Write tests that are robust to implementation details, fail clearly
  when setup breaks, and are self-explanatory for non-obvious values.


  1. Prefer structural/behavioral checks over brittle string comparisons. For example,
  when testing that a class extends a base class, use `instanceof` (prototype-chain
  check) instead of comparing `constructor.name`, since...'
repository: decolua/9router#MARKER9ROUTER7
label: Testing
language: JavaScript
comments_count: 3
repository_stars: 31425
---

Write tests that are robust to implementation details, fail clearly when setup breaks, and are self-explanatory for non-obvious values.

1. Prefer structural/behavioral checks over brittle string comparisons. For example, when testing that a class extends a base class, use `instanceof` (prototype-chain check) instead of comparing `constructor.name`, since the latter breaks under minification, renaming, or further subclassing:
```js
// Avoid
assert.equal(inst.constructor.name, "KimchiExecutor");

// Prefer
assert.ok(inst instanceof DefaultExecutor);
```

2. Load shared fixtures, modules, or registry entries in a `before`/`beforeEach` hook rather than inline inside an `it()` block. This way, if the load fails, it surfaces as a single clear failure instead of cascading into confusing `undefined` assertion errors across unrelated tests.

3. When an assertion depends on a non-obvious derived value (e.g., a constant buffer or offset added by implementation code), add an inline comment explaining where the number comes from, so future readers don't have to trace through the source to understand the expected value:
```js
// handleNonStreamingResponse adds a +2000 buffer via addBufferToUsage
// before returning, so 15 input_tokens becomes 2015 here.
expect(json.usage).toEqual({ input_tokens: 2015, output_tokens: 8 });
```

Applying these practices keeps test failures actionable and prevents wasted debugging time caused by fragile checks, cascading failures, or unexplained magic values.