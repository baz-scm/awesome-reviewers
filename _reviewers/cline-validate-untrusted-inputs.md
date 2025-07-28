---
title: validate untrusted inputs
description: Always validate and sanitize untrusted inputs to prevent injection attacks
  and security vulnerabilities. This includes path inputs that could lead to directory
  traversal attacks and content that may contain malicious HTML entities.
repository: cline/cline
label: Security
language: TypeScript
comments_count: 3
repository_stars: 48299
---

Always validate and sanitize untrusted inputs to prevent injection attacks and security vulnerabilities. This includes path inputs that could lead to directory traversal attacks and content that may contain malicious HTML entities.

For path validation, avoid resolving symbolic links directly as this can enable directory traversal attacks. Instead, use safe path manipulation methods that don't follow symlinks.

For content validation, implement reusable functions to check for dangerous patterns rather than repeating validation logic:

```js
function areUnallowedHtmlEntities(content) {
   const entityNamesToBeBypassed = ['gt','lt','quot','amp','apos']
   const unallowedEntityNamesRegExp = entityNamesToBeBypassed.map(entityName => `(${entityName})`).join('|')
   const reg = new RegExp(`&${unallowedEntityNamesRegExp};`,'g')
   return content.match(reg)?.length > 0
}

// Usage
if(areUnallowedHtmlEntities(content)) {
   // Handle unsafe content
}
```

This approach prevents XSS vulnerabilities while maintaining clean, reusable code. Always assume inputs are malicious and validate accordingly.