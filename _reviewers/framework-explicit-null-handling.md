---
title: Explicit null handling
description: 'Use explicit identity comparisons for null checks and leverage modern
  PHP null-handling features to create more reliable, readable code.


  ## Key practices:'
repository: laravel/framework
label: Null Handling
language: PHP
comments_count: 9
repository_stars: 33763
---

Use explicit identity comparisons for null checks and leverage modern PHP null-handling features to create more reliable, readable code.

## Key practices:

### 1. Use identity operators for null checks instead of functions

```php
// Avoid
if (is_null($value)) { ... }
if (empty($path)) { ... }

// Prefer
if ($value === null) { ... }
if ($path === '') { ... }
if ($array === []) { ... }
```

Identity comparisons (`===`, `!==`) are more precise than functions like `is_null()` or `empty()`. They clearly communicate your intent and avoid unexpected behavior with falsy values like `'0'` or `0`.

### 2. Leverage null coalescing operators

```php
// Avoid
$name = (string) (is_null($this->argument('name')) 
    ? $choice 
    : $this->argument('name'));

// Prefer
$name = (string) ($this->argument('name') ?? $choice);
```

The null coalescing operator (`??`) simplifies conditional logic and makes your code more concise and readable.

### 3. Add proper null annotations in docblocks and types

```php
// Avoid
/** @param string $string The input string to sanitize. */
public static function sanitize($string) 
{
    if ($string === null) {
        return null;
    }
}

// Prefer
/** @param string|null $string The input string to sanitize. */
/** @return string|null The sanitized string. */
public static function sanitize(?string $string) 
{
    if ($string === null) {
        return null;
    }
}
```

Accurately document nullable parameters and return types for better static analysis and IDE support.

### 4. Check for null before method calls

```php
// Avoid direct method calls on possibly null values
$using($this->app);

// Prefer
if ($using !== null) {
    $this->app->call($using);
}
```

Always check if variables are null before calling methods on them to prevent null reference exceptions.

### 5. Be careful with null in array and object relationships

```php
// Check if a relation exists before accessing properties
if (isset($relation)) {
    $attributes[$key] = $relation;
}
```

Remember that `isset()` returns false for null values, which may not be what you expect when working with relationships or arrays that might legitimately contain null values.
