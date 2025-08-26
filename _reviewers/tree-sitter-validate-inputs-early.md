---
title: validate inputs early
description: Functions should validate input parameters at the beginning and return
  appropriate error indicators (like false, null, or error codes) rather than proceeding
  with invalid data. This prevents downstream errors and provides clear feedback to
  callers about invalid usage.
repository: tree-sitter/tree-sitter
label: Error Handling
language: C
comments_count: 2
repository_stars: 21799
---

Functions should validate input parameters at the beginning and return appropriate error indicators (like false, null, or error codes) rather than proceeding with invalid data. This prevents downstream errors and provides clear feedback to callers about invalid usage.

Additionally, ensure error states are properly scoped to avoid misleading results when using shared resources or global state. Error status should accurately reflect the state of the specific operation or object being queried.

Example of early input validation with error return:
```c
bool ts_query_cursor_set_byte_range(
  TSQueryCursor *self,
  uint32_t start_byte,
  uint32_t end_byte
) {
  if (end_byte == 0) {
    end_byte = UINT32_MAX;
  } else if (start_byte > end_byte) {
    return false;  // Early validation with clear error signal
  }
  // ... proceed with valid inputs
}
```

This approach makes error conditions explicit and prevents functions from operating on invalid data, leading to more predictable and debuggable code.