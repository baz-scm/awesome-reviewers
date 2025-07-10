---
title: Ensure test isolation
description: 'Tests should be independent and isolated from each other to prevent
  state leakage and ensure reliable results. When testing components that maintain
  state (like singletons) or require specific environments (like PHP version-specific
  features), choose appropriate isolation strategies:'
repository: getsentry/sentry-php
label: Testing
language: Other
comments_count: 2
repository_stars: 1873
---

Tests should be independent and isolated from each other to prevent state leakage and ensure reliable results. When testing components that maintain state (like singletons) or require specific environments (like PHP version-specific features), choose appropriate isolation strategies:

1. For version-specific language features, isolate them in separate files:
```php
// Place in separate file: Php81/Enums/Status.php
enum Status {
    case Active;
    case Inactive;
}

// In your test file: Php81/YourTest.php
/**
 * @requires PHP 8.1
 */
public function testWithEnum() {
    $status = Status::Active;
    // Test implementation
}
```

2. For stateful components:
   - Use PHPT tests for complete isolation when dealing with singletons or global state
   - Implement tearDown methods that reset state between PHPUnit tests
   - Consider using reflection to reset private/protected properties in singletons

Failing to maintain test isolation can lead to inconsistent results, false positives/negatives, and tests that pass or fail based on execution order rather than correctness.