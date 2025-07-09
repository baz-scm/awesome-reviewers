---
title: Configuration context alignment
description: 'Choose the appropriate configuration context based on how changes will
  be handled by the system. When defining custom configuration variables:


  1. Use `PGC_POSTMASTER` for options that require a server restart or cannot be changed
  while the server is running'
repository: neondatabase/neon
label: Configurations
language: C
comments_count: 3
repository_stars: 19015
---

Choose the appropriate configuration context based on how changes will be handled by the system. When defining custom configuration variables:

1. Use `PGC_POSTMASTER` for options that require a server restart or cannot be changed while the server is running
2. Use `PGC_SIGHUP` only when there is code to properly handle configuration changes at runtime
3. Implement appropriate handler functions for configurations that need special processing when changed

Example of proper context selection:

```c
DefineCustomStringVariable(
    "neon.safekeeper_extra_conninfo_options",
    "libpq keyword parameters and values to apply to safekeeper connections",
    NULL,
    &safekeeper_extra_conninfo_options,
    "",
    PGC_POSTMASTER,  // Requires restart since we don't have reconnection code
    ...
);

// For configurations that need special handling when changed:
DefineCustomStringVariable(
    "neon.safekeepers",
    "List of safekeepers",
    NULL,
    &safekeepers_list,
    "",
    PGC_SIGHUP,  // Can change during runtime
    ...
    NULL, assign_neon_safekeepers, NULL  // Custom handler function
);
```

Adding clear comments when configurations have special behavior enhances code maintainability.