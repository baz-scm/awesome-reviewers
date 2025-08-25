---
title: optimize data structure choices
description: Choose data structures that optimize for your access patterns and computational
  complexity requirements. When you need frequent membership testing or existence
  checking, prefer Set over Array to achieve O(1) lookup complexity instead of O(n)
  linear scanning.
repository: discourse/discourse
label: Algorithms
language: Ruby
comments_count: 2
repository_stars: 44898
---

Choose data structures that optimize for your access patterns and computational complexity requirements. When you need frequent membership testing or existence checking, prefer Set over Array to achieve O(1) lookup complexity instead of O(n) linear scanning.

Key optimizations to consider:
- Replace Array with Set when doing frequent `include?` operations
- Use Set's `add?` method to efficiently combine existence checking with insertion
- Consider the time complexity of your chosen data structure's operations

Example transformation:
```ruby
# Instead of O(n) array scanning:
HUMANIZED_ACRONYMS_HASH = HUMANIZED_ACRONYMS.map { |a| [a, true] }.to_h.freeze

# Use O(1) Set operations:
HUMANIZED_ACRONYMS_SET = HUMANIZED_ACRONYMS.to_set.freeze
```

For existence checking with conditional insertion:
```ruby
# Instead of separate check and add:
next if existing_moderation_groups.include?([category_id, group_id])
existing_moderation_groups.add([category_id, group_id])

# Use Set's efficient add? method:
next unless existing_moderation_groups.add?([category_id, group_id])
```

This approach reduces algorithmic complexity and improves performance, especially as data sets grow larger.