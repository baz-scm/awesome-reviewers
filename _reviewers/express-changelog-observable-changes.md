---
title: Changelog observable changes
description: When documenting dependency updates in History.md/CHANGELOG, only list
  the sub-changes that are actually observable to consumers of this module's public
  API — not every change present in the dependency's own changelog. Before adding
  a bullet, verify whether the change affects how users interact with this module;
  if it doesn't (e.g., the dependency dropped...
repository: Expressjs/Express
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 69580
---

When documenting dependency updates in History.md/CHANGELOG, only list the sub-changes that are actually observable to consumers of this module's public API — not every change present in the dependency's own changelog. Before adding a bullet, verify whether the change affects how users interact with this module; if it doesn't (e.g., the dependency dropped support for a very old Node.js version that this module never supported anyway), omit it. If a change is observable but unlikely to be noticed by most users, still include it — noticeability is absolute, not a popularity measure (e.g., a renamed HTTP status message text, or a transitive dependency version bump like proxy-addr pulling in a new ipaddr.js version, should be listed even if few users will see the difference). Cross-check previous changelog entries for the expected format when describing such transitive/indirect changes.

Example:
```
* deps: proxy-addr@2.0.6
  - deps: ipaddr.js@1.9.1
```
rather than listing unrelated internal changes from the dependency that don't affect Express's API surface.