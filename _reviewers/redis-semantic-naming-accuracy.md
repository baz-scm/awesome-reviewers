---
title: Semantic Naming Accuracy
description: 'Ensure names and naming-related metadata are semantically accurate and
  unambiguous.


  - Don’t reuse a helper/identifier whose name is tied to a specific command if it
  creates confusion. Prefer a dedicated, clearly named function per command.'
repository: redis/redis
label: Naming Conventions
language: Json
comments_count: 2
repository_stars: 74261
---

Ensure names and naming-related metadata are semantically accurate and unambiguous.

- Don’t reuse a helper/identifier whose name is tied to a specific command if it creates confusion. Prefer a dedicated, clearly named function per command.
- Don’t use broad or incorrect category/type metadata fields. If a field conveys the key/type “group”, set it to the actual applicable value.

Example (command-specific key helper):
```js
// Avoid ambiguity: do not reuse sintercardGetKeys for SUNIONCARD
function sintercardGetKeys(...) { /* keys for SINTERCARD */ }
function sunioncardGetKeys(...) { /* keys for SUNIONCARD */ }
```

Example (correct semantic metadata):
```json
{
  "GCRA": {
    "group": "string"
  }
}
```