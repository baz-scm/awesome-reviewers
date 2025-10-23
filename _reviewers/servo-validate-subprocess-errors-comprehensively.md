---
title: validate subprocess errors comprehensively
description: When executing external commands via subprocess, don't rely solely on
  return codes for error detection. Some tools may return 0 even when they fail. Instead,
  check multiple error indicators including return codes, stderr output, and stdout
  content to ensure robust error handling.
repository: servo/servo
label: Error Handling
language: Python
comments_count: 2
repository_stars: 32962
---

When executing external commands via subprocess, don't rely solely on return codes for error detection. Some tools may return 0 even when they fail. Instead, check multiple error indicators including return codes, stderr output, and stdout content to ensure robust error handling.

Use higher-level subprocess methods like `subprocess.run()` or `subprocess.check_output()` when possible, as they provide better built-in error handling. When using `subprocess.Popen()`, always examine both the return code and error output:

```python
# Instead of only checking return code:
if self.hdc_process.returncode != 0:
    logging.warning(f"HDC reverse port forwarding failed: {stderr.decode()}")

# Check both return code AND error message content:
stdout, stderr = self.hdc_process.communicate()
if self.hdc_process.returncode != 0 or "error" in stderr.decode().lower():
    logging.warning(f"HDC reverse port forwarding failed: {stderr.decode()}")
    return False
```

This approach is especially important when working with external tools that may not follow standard Unix conventions for exit codes.