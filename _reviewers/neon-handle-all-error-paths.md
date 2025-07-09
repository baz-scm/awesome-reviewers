---
title: Handle all error paths
description: 'Ensure comprehensive error handling throughout the codebase by implementing
  proper error handling blocks, defensive validation, and thorough resource cleanup. '
repository: neondatabase/neon
label: Error Handling
language: C
comments_count: 3
repository_stars: 19015
---

Ensure comprehensive error handling throughout the codebase by implementing proper error handling blocks, defensive validation, and thorough resource cleanup. 

Three critical aspects to implement:

1. Use proper error handling blocks (PG_TRY/PG_CATCH) to catch and handle exceptions, while ensuring critical cleanup code runs in all scenarios:

```c
PG_TRY();
{
    before_shmem_exit(cleanup_function, data);
    // ... operation that might fail ...
    cancel_before_shmem_exit(cleanup_function, data);
}
PG_CATCH();
{
    cancel_before_shmem_exit(cleanup_function, data);
    // Critical cleanup that must happen regardless of error
    HOLD_INTERRUPTS();
    page_server->disconnect(shard_no);
    RESUME_INTERRUPTS();
    
    PG_RE_THROW();
}
PG_END_TRY();
```

2. Add defensive validation with assertions to catch unexpected conditions early, especially in debug builds:

```c
if (slot->response->tag == T_NeonErrorResponse)
    continue;
// Add assertion to validate expected state
Assert(slot->response->tag == T_NeonGetPageResponse);
```

3. Always validate inputs thoroughly, generating proper errors instead of allowing potential crashes:

```c
if (strncmp(safekeepers_list, "g#", 2) == 0) {
    errno = 0;
    *generation = strtoul(safekeepers_list + 2, &endptr, 10);
    if (errno != 0) {
        wp_log(FATAL, "failed to parse neon.safekeepers generation number: %m");
    }
    // Validate we have the expected format before proceeding
    if (*endptr != ':') {
        wp_log(FATAL, "invalid format in neon.safekeepers, expected 'g#NUMBER:' format");
    }
    return endptr + 1;
}
```

Remember that graceful error handling is always preferable to crashes or undefined behavior. Even if certain conditions "should never happen" based on program logic, add appropriate validation and error handling.