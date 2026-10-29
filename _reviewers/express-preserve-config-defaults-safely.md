---
title: Preserve config defaults safely
description: 'When adding or modifying configuration settings, treat default values
  as part of the public API: do not silently change an existing default (e.g. bumping
  a parser limit from 1000 to 10000) unless the change is intentional and documented.
  If a default behavior must change, add a deprecation warning that fires only when
  the application relies on the implicit...'
repository: Expressjs/Express
label: Configurations
language: JavaScript
comments_count: 3
repository_stars: 69580
---

When adding or modifying configuration settings, treat default values as part of the public API: do not silently change an existing default (e.g. bumping a parser limit from 1000 to 10000) unless the change is intentional and documented. If a default behavior must change, add a deprecation warning that fires only when the application relies on the implicit default, not when the user has explicitly set that value — track this with an internal flag rather than inferring intent from the chosen value.

```js
// Track whether the user explicitly configured the setting
var usingDefaultExtendedParser = true;

app.set('query parser', function (val) {
  usingDefaultExtendedParser = false; // user made an explicit choice
  return parseExtendedQueryString(val);
});

// Only warn when no explicit choice was made
if (usingDefaultExtendedParser) {
  deprecate('default extended query parser is deprecated, set explicitly to override');
}
```

Additionally, always read or write configuration through the established accessor functions (`app.get()` / `app.set()`) rather than touching the internal settings object directly (e.g. `app.settings.etag`). Direct property access bypasses validation/defaults handling and was deprecated for this reason — use `app.get('etag')` instead.</description>
</invoke>
