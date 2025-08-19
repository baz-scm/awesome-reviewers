---
title: consistent formatting rules
description: Maintain consistent formatting throughout the codebase to improve readability
  and maintainability. This includes standardizing function declaration spacing, comment
  styles, pointer/reference formatting, and type naming conventions.
repository: ClickHouse/ClickHouse
label: Code Style
language: Other
comments_count: 3
repository_stars: 42425
---

Maintain consistent formatting throughout the codebase to improve readability and maintainability. This includes standardizing function declaration spacing, comment styles, pointer/reference formatting, and type naming conventions.

Key formatting rules to follow:

1. **Function declarations**: Use consistent spacing around braces and parameters
```cpp
// Preferred - consistent spacing
const NATSConnectionPtr & getConnection() { return connection; }
const std::vector<String> & getSubjects() const { return subjects; }

// Avoid - inconsistent spacing  
const NATSConnectionPtr & getConnection(){return connection;}
const String & getQueueName() const{return queue_name;}
```

2. **Comments**: Use triple slashes (///) for single-line comments instead of double slashes (//)
```cpp
/// Implements `instrumentation` system table, which allows you to get information about functions instrumented by XRay.
// Avoid: // Get a vector of indices.
```

3. **Pointer and reference formatting**: Add spaces around `*` and `&` operators
```cpp
// Preferred
std::vector<uint32_t> getIndices(const GinFilter * filter, const PostingsCacheForStore * cache_store) const;

// Avoid
std::vector<uint32_t> getIndices(const GinFilter *filter, const PostingsCacheForStore *cache_store) const;
```

4. **Type naming**: Follow project conventions (e.g., `UInt32` instead of `uint32_t` in ClickHouse codebase)

Consistent formatting reduces cognitive load during code reviews and makes the codebase more professional and maintainable.