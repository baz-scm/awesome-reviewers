---
title: Propagate errors with context
description: Always propagate errors appropriately by rethrowing caught exceptions
  and maintaining error context. Catch exceptions only when you can handle them meaningfully,
  and ensure errors aren't silently swallowed.
repository: getsentry/sentry-php
label: Error Handling
language: PHP
comments_count: 5
repository_stars: 1873
---

Always propagate errors appropriately by rethrowing caught exceptions and maintaining error context. Catch exceptions only when you can handle them meaningfully, and ensure errors aren't silently swallowed.

Key principles:
1. Rethrow caught exceptions when you can't handle them
2. Catch \Throwable instead of \Exception for comprehensive error handling
3. Keep exception handling scope narrow and focused
4. Avoid generic catch blocks that mask the original error

Example:
```php
// Bad - Swallowing the error
try {
    $result = $callback();
} catch (\Throwable $e) {
    $status = CheckInStatus::error();
}

// Good - Proper error propagation
try {
    $result = $callback();
} catch (\Throwable $e) {
    $status = CheckInStatus::error();
    throw $e; // Rethrow to maintain error context
}

// Good - Focused exception handling
try {
    $promise->wait();
} catch (\Throwable $e) {
    return null; // Explicit handling with clear intent
}
```