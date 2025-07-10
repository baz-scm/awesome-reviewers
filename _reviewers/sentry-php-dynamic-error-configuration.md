---
title: Dynamic error configuration
description: Design error handling systems that respect runtime changes to error settings
  rather than fixing configurations at initialization time. When handling errors,
  dynamically evaluate error reporting flags to allow for temporary error silencing
  and context-specific error handling behavior. Preserve user-specified error levels
  when processing exceptions to ensure...
repository: getsentry/sentry-php
label: Error Handling
language: Markdown
comments_count: 2
repository_stars: 1873
---

Design error handling systems that respect runtime changes to error settings rather than fixing configurations at initialization time. When handling errors, dynamically evaluate error reporting flags to allow for temporary error silencing and context-specific error handling behavior. Preserve user-specified error levels when processing exceptions to ensure intended error reporting behavior is maintained throughout the error handling pipeline.

```php
// Good: Dynamically evaluate error settings during error handling
function errorHandler($errno, $errstr, $errfile, $errline) {
    // Check current error reporting settings at runtime
    if (!(error_reporting() & $errno)) {
        // Error is silenced with @ operator or error_reporting settings
        return;
    }
    
    // Handle error based on current settings
    // ...
}

// Bad: Fixed error configuration at initialization
$errorTypes = error_reporting(); // Captured once at setup
function badErrorHandler($errno, $errstr, $errfile, $errline) {
    global $errorTypes;
    if (!($errorTypes & $errno)) { // Uses fixed setting from initialization
        return;
    }
    // ...
}
```