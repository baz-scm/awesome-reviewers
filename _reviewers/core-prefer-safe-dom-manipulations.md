---
title: Prefer safe DOM manipulations
description: 'When manipulating DOM content, prefer safer alternatives to innerHTML
  when possible to prevent Cross-Site Scripting (XSS) vulnerabilities. For example,
  when clearing element content, use textContent instead of innerHTML:'
repository: vuejs/core
label: Security
language: TypeScript
comments_count: 2
repository_stars: 50769
---

When manipulating DOM content, prefer safer alternatives to innerHTML when possible to prevent Cross-Site Scripting (XSS) vulnerabilities. For example, when clearing element content, use textContent instead of innerHTML:

```javascript
// Avoid this (potential XSS risk)
container.innerHTML = '';

// Prefer this (safer alternative)
container.textContent = '';
```

For cases where HTML parsing is necessary, implement Trusted Types policies with minimal permissions, defining only the functions you absolutely need (e.g., just createHTML if that's all you're using). When supported by browsers, consider using built-in helpers like emptyHTML() for better performance and security.