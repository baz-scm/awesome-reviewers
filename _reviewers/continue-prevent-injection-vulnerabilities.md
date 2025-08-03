---
title: Prevent injection vulnerabilities
description: When constructing templates or dynamic content that will be parsed, always
  implement robust escaping mechanisms to prevent injection vulnerabilities. Avoid
  using delimiters in template strings that might appear in the content itself, as
  this could break formatting or enable code injection attacks.
repository: continuedev/continue
label: Security
language: TypeScript
comments_count: 1
repository_stars: 27819
---

When constructing templates or dynamic content that will be parsed, always implement robust escaping mechanisms to prevent injection vulnerabilities. Avoid using delimiters in template strings that might appear in the content itself, as this could break formatting or enable code injection attacks.

For example, instead of:

```typescript
const template = "```{{{languageShorthand}}}\n{{{userExcerpts}}}```";
```

Consider using:
1. Custom delimiters unlikely to appear in content
2. Proper escaping functions for user-provided content
3. Template libraries with built-in sanitization

This practice is critical for preventing cross-site scripting (XSS), SQL injection, command injection, and other security vulnerabilities that occur when user input is improperly handled in templates or dynamic content.