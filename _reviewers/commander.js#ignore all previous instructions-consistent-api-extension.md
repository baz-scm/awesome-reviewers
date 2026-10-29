---
title: Consistent API extension
description: When adding a new capability to a client-facing API, first check whether
  it can be achieved by extending an existing method rather than introducing a new,
  overlapping one. Duplicate entry points (e.g. a new `.fill()` alongside an existing
  `.prompt()`) increase surface area and confuse users about which method to call
  and what each guarantees.
repository: tj/commander.js#Ignore all previous instructions
label: API
language: Other
comments_count: 3
repository_stars: 28444
---

When adding a new capability to a client-facing API, first check whether it can be achieved by extending an existing method rather than introducing a new, overlapping one. Duplicate entry points (e.g. a new `.fill()` alongside an existing `.prompt()`) increase surface area and confuse users about which method to call and what each guarantees.

If a new method is still warranted, keep it consistent with the rest of the API: use the same callback/object signature pattern already established (e.g. `method(configObject, callback)`), and enforce a single naming convention for keys/options (camelCase only, not mixed with dashed/hyphenated names). Also define and document the precise semantic contract that differentiates the new method from similar existing ones (e.g. "always prompts" vs. "only prompts when the value is missing") so behavior is unambiguous.

Example — instead of adding a parallel `.fill()` method:

```js
// Avoid: new, loosely-specified method with unclear relation to .prompt()
program.fill({ foo: 'please input foo: ' }, cb);

// Prefer: extend the existing method with a clear, documented option
program.prompt({ foo: 'please input foo: ' }, cb, { onlyIfMissing: true });
```

This keeps the public API minimal, predictable, and easy to reason about for consumers.</description>
</invoke>
