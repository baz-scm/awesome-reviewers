---
title: Check operation failures
description: Always validate inputs and check return values of operations that can
  fail, providing clear error messages when failures occur. This includes system calls,
  library functions, and user input validation.
repository: bazelbuild/bazel
label: Error Handling
language: Other
comments_count: 3
repository_stars: 24489
---

Always validate inputs and check return values of operations that can fail, providing clear error messages when failures occur. This includes system calls, library functions, and user input validation.

For file operations, check return values and handle errors appropriately:
```cpp
FILE* procs = fopen(procs_path, "w");
if (procs != NULL) {
  if (fprintf(procs, "%d", pid) < 0) {
    // Log error and handle failure
  }
  if (fclose(procs) != 0) {
    // Log error and handle failure  
  }
}
```

For input validation, check for invalid states and provide helpful error messages:
```cpp
if (command.empty()) {
  blaze_util::StringPrintf(error, "Command cannot be the empty string (try 'help')");
  return nullptr;
}
```

Additionally, implement proactive measures to prevent predictable failures, such as proper argument escaping before passing to system commands. This defensive approach reduces the likelihood of runtime failures and makes debugging easier when issues do occur.