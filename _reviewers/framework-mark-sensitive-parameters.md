---
title: Mark sensitive parameters
description: Always use the `#[\SensitiveParameter]` attribute for parameters containing
  sensitive information such as passwords, tokens, API keys, and personal identifiable
  information. This prevents accidental exposure of sensitive data in logs, stack
  traces, and debugging information, which could otherwise lead to security breaches.
repository: laravel/framework
label: Security
language: PHP
comments_count: 2
repository_stars: 33763
---

Always use the `#[\SensitiveParameter]` attribute for parameters containing sensitive information such as passwords, tokens, API keys, and personal identifiable information. This prevents accidental exposure of sensitive data in logs, stack traces, and debugging information, which could otherwise lead to security breaches.

```php
// Before - security risk
public function __construct(
    public ?string $username = null,
    public ?string $pass = null,
) {}

// After - secure
public function __construct(
    public ?string $username = null,
    #[\SensitiveParameter]
    public ?string $pass = null,
) {}

// Also use in method parameters
public function validateCredentials(
    $username, 
    #[\SensitiveParameter] $password
) {
    // Password won't appear in logs or stack traces
}
```

For legacy PHP versions without attribute support, consider using alternative patterns such as:
1. Accepting sensitive data through non-logged channels
2. Sanitizing log output manually before writing
3. Using specialized secure input handlers

Additionally, ensure proper error handling for security-critical functions. Avoid using error suppression operators (@) in favor of try-catch blocks that capture errors without exposing implementation details.
