---
title: avoid eval() function
description: The eval() function executes arbitrary JavaScript code from strings,
  creating significant security vulnerabilities including code injection attacks.
  This is especially dangerous when processing external data like API responses, user
  input, or browser logs that could contain malicious code.
repository: facebook/yoga
label: Security
language: TypeScript
comments_count: 1
repository_stars: 18255
---

The eval() function executes arbitrary JavaScript code from strings, creating significant security vulnerabilities including code injection attacks. This is especially dangerous when processing external data like API responses, user input, or browser logs that could contain malicious code.

Use safer alternatives for common use cases:
- For JSON parsing: Use JSON.parse() instead of eval()
- For dynamic property access: Use bracket notation or Object.hasOwnProperty()
- For mathematical expressions: Use dedicated math libraries

Example of the security issue:
```javascript
// Dangerous - can execute arbitrary code
const result = eval(logs[0].message.replace(/^[^"]*/, ''));

// Safe - only parses JSON data
const result = JSON.parse(logs[0].message.replace(/^[^"]*/, ''));
```

Modern linters and security scanners typically flag eval() usage. If eval() is absolutely necessary, ensure the input is thoroughly validated and sanitized, though this approach is strongly discouraged.