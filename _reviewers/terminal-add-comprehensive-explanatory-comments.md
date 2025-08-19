---
title: Add comprehensive explanatory comments
description: When code involves complex relationships between multiple components
  or non-obvious usage patterns, add comprehensive explanatory comments that consolidate
  key information in one accessible location. This is especially important for files
  with multiple structs, classes, or APIs that work closely together.
repository: microsoft/terminal
label: Documentation
language: Other
comments_count: 2
repository_stars: 99242
---

When code involves complex relationships between multiple components or non-obvious usage patterns, add comprehensive explanatory comments that consolidate key information in one accessible location. This is especially important for files with multiple structs, classes, or APIs that work closely together.

The comment should explain:
- Relationships and responsibilities between components
- Differences between similar-looking members or methods
- How to properly use the APIs or objects
- What the code enables or prevents

Example for a header file with multiple related structs:
```cpp
/*
 * Media Resource Management System
 * 
 * This file contains structs that work together to handle media resources:
 * - MediaResource: Represents a media file with both original and resolved paths
 *   - 'ok' indicates if the resource was found, 'resolved' indicates if path resolution succeeded
 *   - 'value' is the original path, 'resolvedValue' is the absolute/canonical path
 * - MediaResourceManager: Handles loading and caching of MediaResource objects
 * 
 * Usage: Create MediaResource objects through MediaResourceManager.load() to ensure
 * proper path resolution and caching. Direct construction bypasses validation.
 */
```

Avoid scattering this information across PR descriptions, comments, or other files. Centralize it where developers will naturally look when working with the code.