---
title: Sanitize untrusted input
description: Always sanitize or escape untrusted input before using it in security-sensitive
  contexts to prevent injection attacks. This includes HTML content that could lead
  to XSS vulnerabilities and user-provided strings used in regex patterns.
repository: block/goose
label: Security
language: TSX
comments_count: 2
repository_stars: 19037
---

Always sanitize or escape untrusted input before using it in security-sensitive contexts to prevent injection attacks. This includes HTML content that could lead to XSS vulnerabilities and user-provided strings used in regex patterns.

For HTML content, avoid directly rendering untrusted data. Instead of passing raw HTML to iframe srcdoc or similar contexts, use a component library with controlled inputs or implement proper HTML escaping.

For regex patterns, escape special characters in user input before using it in regex construction:

{% raw %}
```javascript
// Vulnerable - user input could inject regex patterns
const regex = new RegExp(`{{${userKey}}}`);

// Safe - escape special characters to treat input as literal text
const regex = new RegExp(`{{\s*${userKey.replace(/[.*+?^${}()|[\]\\]/g, '\$&')}\s*}}`, 'g');
```
{% endraw %}

Consider the security implications of any user-controlled data and apply appropriate sanitization based on the context where it will be used.
