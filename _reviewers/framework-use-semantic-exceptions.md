---
title: Use semantic exceptions
description: Choose exception types that accurately reflect the nature of the error.
  Use `LogicException` for developer errors like incorrect usage, `InvalidArgumentException`
  for invalid inputs, `OutOfBoundsException` for range violations, and specialized
  exceptions for domain-specific errors.
repository: laravel/framework
label: Error Handling
language: PHP
comments_count: 8
repository_stars: 33763
---

Choose exception types that accurately reflect the nature of the error. Use `LogicException` for developer errors like incorrect usage, `InvalidArgumentException` for invalid inputs, `OutOfBoundsException` for range violations, and specialized exceptions for domain-specific errors.

This improves error diagnostics, enables selective exception handling, and communicates intent more clearly than using generic exceptions or returning magic values.

```php
// Instead of this
throw new Exception("Invalid compression mode");

// Do this
if ($mode < 1 || $mode > 9) {
    throw new OutOfBoundsException('Compression mode must be between 1 and 9.');
}

// Instead of this
throw (new ModelNotFoundException)->setModel(get_class($this), $value);

// Do this
throw (new InvalidIdFormatException)->setModel(get_class($this), $value);

// Instead of using assertions that may be disabled
assert(is_object($model), 'Resource collection guesser expects objects.');

// Do this
if (!is_object($model)) {
    throw new InvalidArgumentException('Resource collection guesser expects objects.');
}

// For related exceptions, create hierarchies for better error handling
class ViteException extends Exception {}
class ViteManifestNotFoundException extends ViteException {}
```

When creating exception hierarchies, consider extending from framework exceptions like `HttpException` for web applications to ensure proper HTTP status codes are returned. This allows consumers to handle entire categories of errors with a single catch block while still providing appropriate responses.

Good exception selection is the foundation of effective error handling and leads to more maintainable, self-documenting code.
