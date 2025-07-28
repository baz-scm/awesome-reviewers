---
title: use logging over print
description: Replace all `print()` statements with appropriate logging calls using
  Python's built-in logging module. This applies to debug output, informational messages,
  and error reporting. Print statements should be reserved only for direct user interaction
  or when logging infrastructure is not available.
repository: comfyanonymous/ComfyUI
label: Logging
language: Python
comments_count: 4
repository_stars: 83726
---

Replace all `print()` statements with appropriate logging calls using Python's built-in logging module. This applies to debug output, informational messages, and error reporting. Print statements should be reserved only for direct user interaction or when logging infrastructure is not available.

Use appropriate logging levels:
- `logging.debug()` for debug information
- `logging.info()` for general informational messages  
- `logging.warning()` for warnings
- `logging.error()` for error conditions

Example transformation:
```python
# Instead of:
print(f"Error reading version in get_workflow_templates_version: {e}")
print("Single LLAMA3_8 for HiDreams")
print(mask.shape)

# Use:
logging.error(f"Error reading version in get_workflow_templates_version: {e}")
logging.info("Single LLAMA3_8 for HiDreams")
logging.debug(f"Mask shape: {mask.shape}")
```

This ensures consistent log formatting, proper log levels, and enables centralized log management and filtering. Remove debug print statements entirely when they're no longer needed, and ensure you're using Python's standard `logging` module rather than custom logging libraries.