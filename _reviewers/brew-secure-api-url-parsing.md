---
title: Secure API URL parsing
description: 'When parsing API endpoint URLs, implement rigorous input validation
  using precise regular expressions. This includes:

  - Escaping special characters in domain literals (e.g., `github\.com`)'
repository: Homebrew/brew
label: API
language: Shell
comments_count: 3
repository_stars: 44168
---

When parsing API endpoint URLs, implement rigorous input validation using precise regular expressions. This includes:
- Escaping special characters in domain literals (e.g., `github\.com`)
- Excluding URL separators (like /, ?, #) from username/password patterns
- Restricting allowed characters for security-sensitive components like API keys
- Minimizing unnecessary capture groups to improve clarity and performance

For example, instead of:
```bash
[[ "${API_URL}" =~ https://(([^:@]+)(:([^@]+))?@)?github.com/(.*)$ ]]
```

Use a more precise pattern:
```bash
[[ "${API_URL}" =~ https://(([^:@/?#]+)(:([^@/?#]+))?@)?github\.com/(.*)$ ]]
```

For API keys or tokens, consider restricting to known valid formats:
```bash
[[ "${API_TOKEN}" =~ ^[[:alnum:]_]+$ ]]
```

This approach prevents security vulnerabilities and ensures consistent API authentication handling across your application.