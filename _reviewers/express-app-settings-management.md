---
title: App settings management
description: 'Treat application settings as a well-defined, centrally managed API
  rather than ad-hoc values scattered through the codebase.


  - Always read and write settings through the accessor methods (`app.set()` / `app.get()`),
  never via direct object access like `app.settings.foo`; direct access bypasses validation
  and has been deprecated since 3.0.'
repository: expressjs/Express
label: Configurations
language: JavaScript
comments_count: 5
repository_stars: 69579
---

Treat application settings as a well-defined, centrally managed API rather than ad-hoc values scattered through the codebase.

- Always read and write settings through the accessor methods (`app.set()` / `app.get()`), never via direct object access like `app.settings.foo`; direct access bypasses validation and has been deprecated since 3.0.
- Define default values for every setting once, in the central `defaultConfiguration` (or equivalent), instead of inlining fallback logic at each call site. For example, set `app.set('jsonp callback name', 'callback')` in `defaultConfiguration` rather than doing `this.req.query[app.get('jsonp callback name') || 'callback']` wherever it's needed.
- Validate and normalize values before they are passed to sub-modules or middleware options. Settings like `etag` must resolve to an actual boolean before being forwarded (`opts.etag = !!app.get('etag')`), since passing `undefined` or non-boolean values invites undefined behavior downstream.
- When introducing a new setting or changing a default (e.g., a parser limit), preserve the previously shipped default value unless there is an explicit, documented reason to change it, so existing applications don't silently change behavior after an upgrade.
- Prefer explicit, stable tracking flags/properties for feature detection over relying on implementation details such as `fn.name`, which can be altered by minifiers/bundlers and break silently in production.

Following these rules keeps configuration behavior predictable, backward-compatible, and easy to reason about across the framework and its middleware.</description>
</invoke>
