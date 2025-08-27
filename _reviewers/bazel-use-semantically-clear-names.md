---
title: Use semantically clear names
description: Choose names that clearly express their purpose and avoid patterns that
  can lead to confusion or bugs. Names should be self-documenting and unambiguous
  in their meaning.
repository: bazelbuild/bazel
label: Naming Conventions
language: Other
comments_count: 5
repository_stars: 24489
---

Choose names that clearly express their purpose and avoid patterns that can lead to confusion or bugs. Names should be self-documenting and unambiguous in their meaning.

Key principles:
- **Avoid double negatives**: Use positive method names like `IsKnown()` instead of `!IsUnknown()` to prevent logical errors
- **Use unambiguous values**: Start counters from 1 instead of 0 when 0 could mean "unset" (e.g., `attempt_number` starting from 1 vs `retry_attempt` starting from 0)
- **Drop implementation details**: Remove internal suffixes like `_src` from public-facing names
- **Use accurate spelling**: Fix typos like `ASSESMBLER_WITH_C_PREPROCESSOR` → `ASSEMBLER_WITH_C_PREPROCESSOR`
- **Generalize when appropriate**: Rename `_is_versioned_shared_library_extension_valid` to `_is_versioned_library_extension_valid` for broader applicability

Example of avoiding double negatives:
```cpp
// Confusing - double negative can lead to bugs
if (!command_wait_duration_ms.IsUnknown()) {
    // This was actually a bug in the original code
}

// Clear - positive logic is easier to understand
if (command_wait_duration_ms.IsKnown()) {
    // Intent is immediately clear
}
```

Example of unambiguous field naming:
```proto
// Ambiguous - 0 could mean "first attempt" or "field not supported"
int32 retry_attempt = 8;  // starts from 0

// Clear - distinguishes between first attempt vs unsupported field
int32 stream_attempt_number = 8;  // starts from 1
```