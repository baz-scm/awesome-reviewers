---
title: Complete null checks
description: Always perform thorough null checks before dereferencing pointers, and
  ensure all operations on potentially null objects are contained within the null
  check block. This prevents null pointer dereferences and undefined behavior.
repository: ollama/ollama
label: Null Handling
language: C++
comments_count: 3
repository_stars: 145705
---

Always perform thorough null checks before dereferencing pointers, and ensure all operations on potentially null objects are contained within the null check block. This prevents null pointer dereferences and undefined behavior.

For example, when freeing resources, place all cleanup operations inside the null check:

```cpp
// Bad - operations outside null check
if (g != nullptr) {
    delete g->vocab;
    // Other operations...
}
g->someOperation(); // Potential null dereference!

// Good - all operations inside null check
if (g != nullptr) {
    delete g->vocab;
    g->someOperation(); 
    // All operations safely inside the check
}
```

When working with references or pointers that may become invalid, consider returning objects by value instead of by reference to prevent dangling references. This applies especially when the object lifetime cannot be guaranteed:

```cpp
// Risky - caller might use reference after source is deallocated
const std::string & token_to_piece(uint32_t token);

// Safer - returns a copy that remains valid
const std::string token_to_piece(uint32_t token);
```