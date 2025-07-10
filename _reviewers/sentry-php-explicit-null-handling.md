---
title: Explicit null handling
description: Always be explicit and consistent when handling null values to improve
  code clarity and prevent subtle bugs. This applies to null checks, nullable type
  declarations, and function parameters.
repository: getsentry/sentry-php
label: Null Handling
language: PHP
comments_count: 6
repository_stars: 1873
---

Always be explicit and consistent when handling null values to improve code clarity and prevent subtle bugs. This applies to null checks, nullable type declarations, and function parameters.

**For null checks:**
- Use explicit comparisons with null rather than relying on truthiness checks
- Write `null !== $variable` or `$variable === null` instead of just `if ($variable)`
- Avoid variable assignments within conditional statements when checking for null

**For type declarations:**
- Always use the nullable operator (`?`) for parameters and return types that can be null
- Make docblocks consistent with type declarations by documenting nullable types
- Ensure parameters with null defaults are always declared as nullable

**For function parameters:**
- If a parameter is optional and can be null, make it both nullable and provide a default
- Be consistent with parameter nullability across similar functions

```php
// Bad
public function doSomething($client)
{
    if ($client) {
        // ...
    }
}

// Good
public function doSomething(?ClientInterface $client = null): ?string
{
    if (null !== $client) {
        // ...
    }
}
```

This pattern makes intent clear, improves static analysis capabilities, and provides better autocomplete support in IDEs. It also prevents confusion between false, empty strings, zero, and null values in conditionals.