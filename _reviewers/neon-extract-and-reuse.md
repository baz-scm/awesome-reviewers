---
title: Extract and reuse
description: Create focused utility functions for repeated or complex operations instead
  of duplicating logic across the codebase. When implementing functionality, first
  check if similar code already exists that can be reused.
repository: neondatabase/neon
label: Code Style
language: C
comments_count: 3
repository_stars: 19015
---

Create focused utility functions for repeated or complex operations instead of duplicating logic across the codebase. When implementing functionality, first check if similar code already exists that can be reused.

Benefits:
- Improves code readability by abstracting implementation details
- Reduces duplication, making maintenance easier
- Makes testing isolated functionality simpler

Example:
```c
// Before: Repeated parsing logic in multiple places
if (strncmp(wp->config->safekeeper_connstrings, "g#", 2) == 0)
{
    char *endptr;
    errno = 0;
    wp->safekeepers_generation = strtoul(wp->config->safekeeper_connstrings + 2, &endptr, 10);
    if (errno != 0)
    {
        wp_log(FATAL, "failed to parse generation number: %m");
    }
    // ...
}

// After: Extracted to a utility function
bool split_off_safekeepers_generation(const char* connstring, 
                                      uint32* generation, 
                                      const char** remaining)
{
    if (strncmp(connstring, "g#", 2) == 0)
    {
        char *endptr;
        errno = 0;
        *generation = strtoul(connstring + 2, &endptr, 10);
        if (errno != 0 || *endptr != ':')
            return false;
        
        *remaining = endptr + 1;
        return true;
    }
    *generation = INVALID_GENERATION;
    *remaining = connstring;
    return true;
}

// Usage
const char* remaining;
if (!split_off_safekeepers_generation(wp->config->safekeeper_connstrings, 
                                     &wp->safekeepers_generation, 
                                     &remaining))
{
    wp_log(FATAL, "failed to parse generation number");
}
```

When implementing new functionality, scan the codebase for similar operations that might already be implemented as utility functions. For complex operations like parsing, prefer creating dedicated functions that can be reused across the project.