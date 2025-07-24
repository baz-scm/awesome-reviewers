---
title: Validate environment variables
description: Always validate environment variables before use and implement proper
  fallback strategies. For required variables, fail fast with clear error messages.
  For optional variables with empty values, ensure they don't short-circuit fallback
  chains.
repository: appwrite/appwrite
label: Configurations
language: PHP
comments_count: 10
repository_stars: 51959
---

Always validate environment variables before use and implement proper fallback strategies. For required variables, fail fast with clear error messages. For optional variables with empty values, ensure they don't short-circuit fallback chains.

```php
// Bad: Empty value leads to malformed URL
$hostname = System::getEnv('_APP_CONSOLE_DOMAIN', System::getEnv('_APP_DOMAIN', ''));

// Good: Check for truthy value before fallback
$hostname = System::getEnv('_APP_CONSOLE_DOMAIN', null);
if (empty($hostname)) {
    $hostname = System::getEnv('_APP_DOMAIN', '');
    if (empty($hostname)) {
        throw new \RuntimeException('Required environment variable _APP_DOMAIN is not set');
    }
}
```

When implementing environment variable handling:
1. For required variables, throw an exception if missing or invalid
2. For optional variables with fallbacks, check for empty strings before using
3. Document all environment variables in .env.example with descriptions and default values
4. For configuration files that consume environment variables, add validation logic
5. Verify type correctness (e.g., using `intval()` for numeric settings, checking IP formats)
6. Add validation for variables containing URLs, file paths, or other structured data