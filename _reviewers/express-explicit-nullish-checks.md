---
title: Explicit nullish checks
description: 'Avoid relying on loose truthiness (`||`, `!x`) when the goal is to detect
  "missing" (`null`/`undefined`) values, since this also matches other valid falsy
  values like `''''`, `0`, and `false`, silently discarding legitimate input. Use
  explicit, strict checks that only target nullish values: `x === undefined`, `x ==
  null` (catches both `null` and `undefined`),...'
repository: expressjs/Express
label: Null Handling
language: JavaScript
comments_count: 10
repository_stars: 69579
---

Avoid relying on loose truthiness (`||`, `!x`) when the goal is to detect "missing" (`null`/`undefined`) values, since this also matches other valid falsy values like `''`, `0`, and `false`, silently discarding legitimate input. Use explicit, strict checks that only target nullish values: `x === undefined`, `x == null` (catches both `null` and `undefined`), or the nullish-coalescing operator `??`/`??=` for defaulting. Only fall back to loose truthiness when every falsy value really should be treated the same way, and document that assumption in a comment.

For example, prefer:
```js
// Only default when the option is genuinely unset, not when it's false
opts.etag ??= this.app.enabled('etag');
```
over an unconditional overwrite that makes an explicit `false`/`null` option unreachable.

Similarly, when merging a proxied header value with a direct one, don't use `host || this.get('Host')`, because an empty-but-present header (`''`) is falsy and would be incorrectly treated as absent. Instead check explicitly for the missing case:
```js
if (host === undefined) {
  host = this.get('Host');
}
```

When accepting external/user input that may be `null`, `undefined`, or an unexpected type, don't silently coerce it (e.g. `String(url)` turning `null` into the literal string `"null"`). Validate explicitly and throw a clear error for invalid/missing values rather than letting a bug produce a bogus but valid-looking result. Likewise, don't guard against `null` by only checking `typeof x === 'object'`, since `typeof null === 'object'`; always combine with an explicit `x != null` check. When branching on type (e.g. `null` vs `boolean`/`number`), prefer separate, explicit conditions over combining them in a ternary, to keep the null case visibly distinct from other falsy-but-valid values.</description>
</invoke>
