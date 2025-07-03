---
title: Cache expensive operations
description: Identify and cache results of expensive operations that may be called
  repeatedly during a request lifecycle, especially recursive functions or operations
  performed in loops. This reduces redundant processing and can significantly improve
  application performance.
repository: laravel/framework
label: Performance Optimization
language: PHP
comments_count: 6
repository_stars: 33763
---

Identify and cache results of expensive operations that may be called repeatedly during a request lifecycle, especially recursive functions or operations performed in loops. This reduces redundant processing and can significantly improve application performance.

For example, when working with trait detection or class hierarchy traversal:

```php
// Instead of repeatedly calling an expensive function
public function isPrunable(): bool
{
    return in_array(Prunable::class, class_uses_recursive(static::class)) || static::isMassPrunable();
}

// Cache the result for the lifetime of the request
protected static $classTraitsCache = [];

public function isPrunable(): bool
{
    $class = static::class;
    
    // Only perform the expensive operation once per class
    if (!isset(static::$classTraitsCache[$class])) {
        static::$classTraitsCache[$class] = class_uses_recursive($class);
    }
    
    return in_array(Prunable::class, static::$classTraitsCache[$class]) || static::isMassPrunable();
}
```

Similarly, when selecting methods for array operations, favor efficient approaches. For instance, use `array_search()` over `array_flip()` followed by key lookup for better performance with large arrays.

When implementing expensive transformations (like `toArray()` on models), use memoization techniques to avoid recalculating the same values multiple times during a single request.
