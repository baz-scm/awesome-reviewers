---
title: "Secure Content-Type validation"
description: "When implementing Content-Type validation, ensure regular expressions start with '^' or include ';?' to properly detect the essence MIME type. Improper validation patterns may create vulnerabilities to CORS attacks."
repository: "fastify/fastify"
label: "Security"
language: "JavaScript"
comments_count: 1
repository_stars: 34000
---

When implementing Content-Type validation, ensure regular expressions start with '^' or include ';?' to properly detect the essence MIME type. Improper validation patterns may create vulnerabilities to CORS attacks. 

For example, instead of using a pattern like:
```js
const contentTypeRegex = /json/;
```

Use one of these more secure approaches:
```js
const contentTypeRegex = /^application\/json/; // Anchoring with ^ ensures exact matches
// OR
const contentTypeRegex = /application\/json;?/; // Including ;? handles parameters properly
```

This ensures that malicious Content-Types like "faketype+json" cannot bypass your security validation mechanisms.