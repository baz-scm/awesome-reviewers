---
title: "Consistent semicolon usage"
description: "Always terminate statements with explicit semicolons to maintain consistency with the existing codebase style. Avoid relying on JavaScript's automatic semicolon insertion (ASI) feature, as this can lead to inconsistent code appearance and potential subtle bugs."
repository: "axios/axios"
label: "Code Style"
language: "TypeScript"
comments_count: 2
repository_stars: 107000
---

Always terminate statements with explicit semicolons to maintain consistency with the existing codebase style. Avoid relying on JavaScript's automatic semicolon insertion (ASI) feature, as this can lead to inconsistent code appearance and potential subtle bugs. Project convention shows that 99% of statements already use explicit semicolons.

Example (incorrect):
```javascript
const headers = new AxiosHeaders({foo: "bar"})
```

Example (correct):
```javascript
const headers = new AxiosHeaders({foo: "bar"});
```