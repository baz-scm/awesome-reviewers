---
title: Use specialized sensitive types
description: When handling sensitive data like encryption keys, choose data types
  based on the data's lifecycle and security requirements. Use specialized types (e.g.,
  `EncryptionKey`) for actual sensitive data that persists in memory, as these provide
  memory locking and secure deletion. Use regular strings only for temporary user
  input that gets immediately processed...
repository: duckdb/duckdb
label: Security
language: Other
comments_count: 2
repository_stars: 32061
---

When handling sensitive data like encryption keys, choose data types based on the data's lifecycle and security requirements. Use specialized types (e.g., `EncryptionKey`) for actual sensitive data that persists in memory, as these provide memory locking and secure deletion. Use regular strings only for temporary user input that gets immediately processed and wiped.

For example:
```cpp
// For temporary user input (acceptable)
string encryption_key;  // User input, immediately wiped

// For actual encryption keys (preferred)
EncryptionKey actual_key;  // Locked memory, secure deletion
```

The distinction matters because temporary user input can be any length and exists briefly, while actual keys should be fixed-size, memory-locked, and securely managed throughout their lifecycle.