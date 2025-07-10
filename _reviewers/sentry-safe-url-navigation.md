---
title: Safe URL navigation
description: Always use sanitized navigation utilities instead of directly manipulating
  `window.location` with potentially user-influenced data to prevent cross-site scripting
  (XSS) vulnerabilities. User-provided values can contain malicious scripts that execute
  when inserted into navigation contexts.
repository: getsentry/sentry
label: Security
language: TSX
comments_count: 1
repository_stars: 41297
---

Always use sanitized navigation utilities instead of directly manipulating `window.location` with potentially user-influenced data to prevent cross-site scripting (XSS) vulnerabilities. User-provided values can contain malicious scripts that execute when inserted into navigation contexts.

**Bad:**
```typescript
window.location.assign(this.newPath); // Dangerous if newPath contains user input
```

**Good:**
```typescript
testableWindowLocation.assign(this.newPath); // Uses a wrapper that sanitizes inputs
```

Use wrapper functions or utilities that perform proper validation and sanitization of URLs before navigation. This approach not only improves security but also makes testing easier by providing a mockable interface for navigation operations.