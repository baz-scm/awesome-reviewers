---
title: Avoid breaking API changes
description: When modifying existing public APIs, always maintain backward compatibility
  to avoid breaking existing users. Breaking changes include altering function signatures,
  removing public functions, or changing function visibility from public to private.
repository: vlang/v
label: API
language: Other
comments_count: 3
repository_stars: 36582
---

When modifying existing public APIs, always maintain backward compatibility to avoid breaking existing users. Breaking changes include altering function signatures, removing public functions, or changing function visibility from public to private.

Instead of making breaking changes:
- Keep the original public function and create new internal implementations
- Add new functions with different names rather than changing existing signatures  
- When refactoring, maintain the public interface while changing internal implementation

For example, when refactoring a public function:

```v
// Instead of changing the signature (breaking change):
// pub fn new_digest(absorption_rate int, hash_size int, suffix u8) !&Digest

// Keep the original public function:
pub fn new_digest(absorption_rate int, hash_size int) !&Digest {
    return new_digest_with_suffix(absorption_rate, hash_size, default_suffix)
}

// Add the new functionality as a separate function:
pub fn new_digest_with_suffix(absorption_rate int, hash_size int, suffix u8) !&Digest {
    // implementation
}
```

When removing public functions, keep them as wrappers that call the new internal implementation. This ensures existing code continues to work while allowing internal refactoring and improvements.