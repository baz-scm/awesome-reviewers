---
title: Document non-intuitive code
description: 'Add clear comments to explain complex logic, function differences, and
  non-obvious implementation details. This is especially important for:


  - Similar functions with subtle differences'
repository: nodejs/node
label: Documentation
language: Other
comments_count: 4
repository_stars: 112178
---

Add clear comments to explain complex logic, function differences, and non-obvious implementation details. This is especially important for:

- Similar functions with subtle differences
- Methods with functionality not obvious from their names
- Blocks of code with specific logic checks
- Functions with complex control flow

When a future developer reads your code, they should understand the reasoning without needing to reverse-engineer the logic. Documentation is particularly valuable for code that will be maintained by others.

For example:

```cpp
// Document differences between similar functions
// hashDigest: Creates a fixed-length hash from input data
// xofHashDigest: Creates an extendable-output function hash with custom length
DataPointer hashDigest(const Buffer<const unsigned char>& data,
                       const EVP_MD* md);
DataPointer xofHashDigest(const Buffer<const unsigned char>& data,
                          const EVP_MD* md,
                          size_t length);

// Explain non-intuitive checks
if (content.front() == '[') {
  // This identifies the start of a section like [section_name]
  // ...
}

// Document complex methods
// InitWldp: Initializes Windows Lockdown Policy features
// Loads required DLLs and resolves function pointers for code integrity checks
void InitWldp(Environment* env) {
  // implementation...
}
```

Prioritize documentation that answers "why" over "what" when the code itself already clearly shows what it's doing.