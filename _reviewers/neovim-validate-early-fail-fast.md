---
title: validate early, fail fast
description: Perform comprehensive input validation and precondition checks at the
  beginning of functions, before executing any operations that could have side effects
  or modify system state. This prevents partial execution, inconsistent states, and
  resource leaks when validation fails.
repository: neovim/neovim
label: Error Handling
language: C
comments_count: 5
repository_stars: 91433
---

Perform comprehensive input validation and precondition checks at the beginning of functions, before executing any operations that could have side effects or modify system state. This prevents partial execution, inconsistent states, and resource leaks when validation fails.

Key principles:
- Validate all input parameters and their types before processing
- Check preconditions and system state before performing operations
- Handle all possible input combinations, not just the expected ones
- Fail immediately when validation fails, before any side effects occur

Example from the codebase:
```c
// BAD: Validation after side effects
FILE *f = fopen(path.data, "w");  // Side effect first
if (f == NULL) {
    return;  // But cursor was already moved
}

// GOOD: Validation before side effects  
if (HAS_KEY(opts, set_extmark, conceal)) {
    if (opts->conceal.type == kObjectTypeBoolean) {
        // Handle boolean case
    } else if (opts->conceal.type == kObjectTypeString) {
        // Handle string case  
    } else {
        // ERROR: type is neither string nor boolean
        goto error;
    }
}
```

This approach prevents crashes, data corruption, and difficult-to-debug partial state changes by catching problems before they can cause damage.