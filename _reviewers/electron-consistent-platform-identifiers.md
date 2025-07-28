---
title: consistent platform identifiers
description: When naming platform identifiers, choose one naming convention and use
  it consistently throughout the codebase. Prefer established ecosystem standards
  when available, such as Node.js `process.platform` values (`win32`, `darwin`, `linux`)
  over custom variations.
repository: electron/electron
label: Naming Conventions
language: Yaml
comments_count: 2
repository_stars: 117644
---

When naming platform identifiers, choose one naming convention and use it consistently throughout the codebase. Prefer established ecosystem standards when available, such as Node.js `process.platform` values (`win32`, `darwin`, `linux`) over custom variations.

Avoid mixing different names for the same platform concept (e.g., `windows`, `win`, `win32` all referring to Windows). This creates confusion and requires unnecessary translation logic.

Example of the problem:
```yaml
# Inconsistent - multiple names for Windows platform
artifact-platform: 'windows'  # in one place
build-key: 'win32'            # in another place  
target: 'win'                 # in yet another place
```

Example of the solution:
```yaml
# Consistent - using Node.js process.platform convention
artifact-platform: 'win32'   # everywhere
build-key: 'win32'           
target: 'win32'              
```

This eliminates the need for conditional transformations like `inputs.artifact-platform == 'windows' && 'win32' || inputs.artifact-platform` and makes the codebase more predictable and maintainable.