---
title: Strict null checks
description: Many reported bugs stemmed from using generic truthy/falsy checks (`!x`,
  `x || y`, ternaries) when the real intent was to detect "missing" (`null`/`undefined`)
  values. Falsy-but-valid values such as `''`, `0`, `false`, or `'0'` were incorrectly
  treated as absent, causing logic errors (e.g. an empty `X-Forwarded-Host` header
  being overwritten, or a `'0'`...
repository: Expressjs/Express
label: Null Handling
language: JavaScript
comments_count: 14
repository_stars: 69580
---

Many reported bugs stemmed from using generic truthy/falsy checks (`!x`, `x || y`, ternaries) when the real intent was to detect "missing" (`null`/`undefined`) values. Falsy-but-valid values such as `''`, `0`, `false`, or `'0'` were incorrectly treated as absent, causing logic errors (e.g. an empty `X-Forwarded-Host` header being overwritten, or a `'0'` response body losing its `Content-Length`).

Apply these rules when handling nullable/optional values:

1. Use explicit comparisons (`=== undefined`, `=== null`, or `x == null` to cover both) instead of `!x` or `x || y` when a falsy-but-valid value must be preserved.
2. Prefer the nullish coalescing operator/assignment (`??`, `??=`) for defaulting, since it only falls back on `null`/`undefined` and leaves other falsy values intact:
   ```js
   // Bad: overwrites valid falsy values (e.g. `etag: false`)
   opts.etag = opts.etag || this.app.enabled('etag');

   // Good: only applies default when unset
   opts.etag ??= this.app.enabled('etag');
   ```
3. Remember that `typeof x === 'object'` is `true` for `null`; always guard separately:
   ```js
   if (options && typeof options === 'object') { ... }
   ```
4. When distinguishing "header/option not provided" from "provided but empty", use `typeof x === 'undefined'` or `x === undefined` rather than a truthy check, and document why:
   ```js
   // '' is a valid but falsy value; only fall back when truly unset
   if (typeof host === 'undefined') {
     host = this.get('Host');
   }
   ```
5. Avoid coercing unknown/null/undefined inputs into stringified placeholders (e.g. `String(null)` -> `"null"`); validate the type explicitly and throw or handle the nullable case intentionally rather than silently producing misleading output.
6. When spreading a potentially-undefined object, no fallback is needed (`{ ...maybeUndefined }` safely yields `{}`), so don't add redundant `|| {}` guards.

Following these patterns prevents silent data corruption, keeps optional/nullable handling predictable, and makes the intent of each null/undefined check explicit to future readers.</description>
