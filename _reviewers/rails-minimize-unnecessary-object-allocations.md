---
title: Minimize unnecessary object allocations
description: Avoid creating unnecessary objects, especially in frequently executed
  code paths. This includes being mindful of implicit object allocations from common
  Ruby operations like array methods, string concatenations, and temporary variable
  creation.
repository: rails/rails
label: Performance Optimization
language: Ruby
comments_count: 6
repository_stars: 57027
---

Avoid creating unnecessary objects, especially in frequently executed code paths. This includes being mindful of implicit object allocations from common Ruby operations like array methods, string concatenations, and temporary variable creation.

Key practices:
1. Avoid unnecessary array allocations from methods like `first(n)`, `flatten`, or `map`
2. Use direct iteration instead of intermediate collections when possible
3. Consider using mutation methods (e.g., `<<`) over concatenation (+) for strings
4. Cache computed values that are reused frequently

Example - Before:
```ruby
def process_items
  first_two = items.first(2)  # Creates new array
  result = first_two.map { |x| x.to_s }  # Creates another array
  result.flatten.compact  # Creates more arrays
end
```

Example - After:
```ruby
def process_items
  result = []
  items.each_with_index do |item, index|
    break if index >= 2
    result << item.to_s  # Single array, built incrementally
  end
  result
end
```

This optimization is especially important in hot code paths, such as request processing or data transformation pipelines, where the cumulative effect of unnecessary allocations can impact performance and trigger more frequent garbage collection.
