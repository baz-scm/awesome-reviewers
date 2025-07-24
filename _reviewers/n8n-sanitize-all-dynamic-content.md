---
title: Sanitize all dynamic content
description: 'Always sanitize dynamic content before rendering to prevent XSS and
  injection attacks. This includes HTML content, CSS styles, and executable scripts.
  Use appropriate sanitization methods based on content type:'
repository: n8n-io/n8n
label: Security
language: Other
comments_count: 6
repository_stars: 122978
---

Always sanitize dynamic content before rendering to prevent XSS and injection attacks. This includes HTML content, CSS styles, and executable scripts. Use appropriate sanitization methods based on content type:

1. For HTML content:
```javascript
// Bad
return props.content.html;

// Good
return DOMPurify.sanitize(props.content.html, {
  ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'span', 'div'],
  ALLOWED_ATTR: ['class']
});
```

2. For template rendering:
```html
<!-- Bad -->
<p>{{{message}}}</p>

<!-- Good -->
<p>{{message}}</p>
```

3. For CSS:
- Use strict whitelisting of allowed properties
- Validate against injection patterns
- Consider using CSS-in-JS solutions with built-in sanitization

4. For scripts:
- Avoid dynamic script execution (new Function(), eval())
- Use strict CSP headers
- Implement proper sandboxing for user-provided code

Never trust user input or third-party content. Always validate and sanitize before rendering.