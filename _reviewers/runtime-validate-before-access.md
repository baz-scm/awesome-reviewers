---
title: Validate before access
description: Always validate parameters and initialize variables before access to
  prevent null dereference and undefined behavior. When handling arrays or pointers,
  require and validate length parameters. For conditionally initialized variables,
  ensure all code paths explicitly set values.
repository: dotnet/runtime
label: Null Handling
language: C
comments_count: 3
repository_stars: 16578
---

Always validate parameters and initialize variables before access to prevent null dereference and undefined behavior. When handling arrays or pointers, require and validate length parameters. For conditionally initialized variables, ensure all code paths explicitly set values.

Example:
```c
// Unsafe: No length validation before indexing
static bool IsPathNotFullyQualified(WCHAR* path)
{
    // Potential null dereference or buffer overflow
    if (path[0] == VOLUME_SEPARATOR_CHAR) return false;
}

// Safe: Length parameter and validation
static bool IsPathNotFullyQualified(WCHAR* path, size_t length)
{
    // Validate before accessing
    if (path == NULL || length < 1) return true;
    if (path[0] == VOLUME_SEPARATOR_CHAR) return false;
}

// For conditional initialization, always set values in all branches:
if (!bitmap_only)
    interface_offsets_full[i] = gklass->interface_offsets_packed[i];
else
    interface_offsets_full[i] = 0; // Prevent uninitialized value use
```

When modifying control flow to prevent null pointer dereferences, add explanatory comments to clarify the safety measures for future maintainers.
