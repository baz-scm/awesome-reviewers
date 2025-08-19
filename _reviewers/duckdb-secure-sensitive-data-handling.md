---
title: secure sensitive data handling
description: When handling sensitive data like encryption keys, passwords, or authentication
  tokens, avoid using standard string types that can be easily copied and may persist
  in memory. Instead, use specialized secure data structures that prevent accidental
  copying and provide controlled memory management.
repository: duckdb/duckdb
label: Security
language: C++
comments_count: 2
repository_stars: 32061
---

When handling sensitive data like encryption keys, passwords, or authentication tokens, avoid using standard string types that can be easily copied and may persist in memory. Instead, use specialized secure data structures that prevent accidental copying and provide controlled memory management.

Key practices:
1. **Use secure data structures**: Replace `std::string` with custom classes that are not copy-constructible and handle their own memory locking/unlocking
2. **Explicit memory clearing**: When you must use standard types temporarily, explicitly clear sensitive data using `fill()` and `clear()` operations
3. **Memory locking**: Use platform-specific functions like `mlock()`/`VirtualLock()` to prevent sensitive data from being paged to disk

Example of problematic code:
```cpp
// BAD: std::string can be easily copied accidentally
std::string encryption_key = user_input;
storage_options.encryption_key = encryption_key; // Creates copy
```

Example of secure handling:
```cpp
// GOOD: Explicit clearing of temporary sensitive data
auto user_key = entry.second.GetValue<string>();
storage_options.encryption_key = user_key;

// Clear the user key from memory
fill(user_key.begin(), user_key.end(), '\0');
user_key.clear();
```

This approach prevents sensitive data from accidentally persisting in memory through unintended copies and reduces the attack surface for memory-based exploits.