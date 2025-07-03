---
title: Precise type annotations
description: 'Always use the most specific and accurate type information possible
  in PHPDoc comments to improve static analysis, IDE autocompletion, and code clarity.
  Pay special attention to array types using appropriate syntax:'
repository: laravel/framework
label: Documentation
language: PHP
comments_count: 8
repository_stars: 33763
---

Always use the most specific and accurate type information possible in PHPDoc comments to improve static analysis, IDE autocompletion, and code clarity. Pay special attention to array types using appropriate syntax:

- For associative arrays with string keys: `array<string, mixed>` instead of just `array`
- For arrays of strings: `string[]` rather than generic `array`
- For complex generics: maintain template type parameters like `Collection<int, TPivotModel>`
- For method parameters accepting string or array of strings: `string|string[]` instead of `string|array`

Include full namespaces in type references (e.g., `\Illuminate\Support\Collection` instead of just `Collection`).

When documenting specialized types, use appropriate annotations:
```php
/**
 * Get JSON casting flags for the specified attribute.
 *
 * @param  string  $key
 * @return int-mask-of<JSON_*>
 */
protected function getJsonCastingFlags($key)
```

Precise type annotations help both developers and tools understand your code better, reducing potential errors and improving maintainability.
