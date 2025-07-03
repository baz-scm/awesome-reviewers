---
title: Design flexible APIs
description: 'When designing APIs, prioritize flexibility and developer experience
  by:


  1. **Accept broader parameter types** - Use `callable` instead of `Closure` to support
  various invocation patterns:'
repository: laravel/framework
label: API
language: PHP
comments_count: 5
repository_stars: 33763
---

When designing APIs, prioritize flexibility and developer experience by:

1. **Accept broader parameter types** - Use `callable` instead of `Closure` to support various invocation patterns:

```php
// Instead of this (restrictive):
public function throw(?Closure $callback = null)

// Do this (flexible):
public function throw(?callable $callback = null)
```

2. **Support fluent method chaining** - Allow methods to return the instance for chainable calls:

```php
// Example from date formatting:
public function format(string $format): static
{
    $this->format = $format;
    return $this;
}

// Usage:
$date->format('Y-m-d')->after('2023-01-01');
```

3. **Accept multiple parameter formats** - Make your API handle different input types intelligently:

```php
// Example with status code handling:
if (is_numeric($callback) || is_string($callback) || is_array($callback)) {
    $callback = static::response($callback);
}
```

4. **Use enums for constrained options** - Instead of arbitrary integers, use typed enums:

```php
// Instead of:
public static function query($array, $encodingType = PHP_QUERY_RFC3986)

// Do this:
public static function query($array, HttpQueryEncoding $encodingType = HttpQueryEncoding::Rfc3986)
```

Flexible APIs improve developer experience by being intuitive, reducing errors, and accommodating different coding styles while maintaining robustness and clarity.
