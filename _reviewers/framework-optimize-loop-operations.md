---
title: Optimize loop operations
description: 'When writing loops, optimize for both readability and performance by
  following these key principles:


  1. **Exit early** when a decision can be made:

  ```php'
repository: laravel/framework
label: Algorithms
language: PHP
comments_count: 4
repository_stars: 33763
---

When writing loops, optimize for both readability and performance by following these key principles:

1. **Exit early** when a decision can be made:
```php
// Instead of this:
foreach ($keys as $key) {
    if (! static::has($array, $key)) {
        $result = false;
    }
}
return $result;

// Do this:
foreach ($keys as $key) {
    if (! static::has($array, $key)) {
        return false;
    }
}
return true;
```

2. **Move invariant operations outside loops**:
```php
// Instead of this:
foreach ($array as $key => $item) {
    $groupKey = is_callable($groupBy) ? $groupBy($item, $key) : static::get($item, $groupBy);
    // ...
}

// Do this:
$groupBy = is_callable($groupBy) ? $groupBy : fn ($item) => static::get($item, $groupBy);
foreach ($array as $key => $item) {
    $groupKey = $groupBy($item, $key);
    // ...
}
```

3. **Use O(1) operations** where possible instead of O(n):
```php
// Instead of this:
if (in_array(InteractsWithQueue::class, $uses) && in_array(Queueable::class, $uses)) {
    // ...
}

// Do this:
if (isset($uses[InteractsWithQueue::class], $uses[Queueable::class])) {
    // ...
}
```

4. **Add early termination conditions** for algorithms that can complete before processing all elements:
```php
// Add early exit:
foreach ($map as $roman => $value) {
    while ($number >= $value) {
        $result .= $roman;
        $number -= $value;
    }
    
    if ($number === 0) {
        return $result;
    }
}
```

These optimizations help reduce computational complexity and unnecessary operations, resulting in more efficient and maintainable code.
