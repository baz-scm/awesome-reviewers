---
title: Use environment variables
description: Make configuration values configurable through environment variables
  with sensible defaults instead of hard-coding them. This improves flexibility and
  testability while maintaining backward compatibility.
repository: commaai/openpilot
label: Configurations
language: Python
comments_count: 5
repository_stars: 58214
---

Make configuration values configurable through environment variables with sensible defaults instead of hard-coding them. This improves flexibility and testability while maintaining backward compatibility.

Use `os.getenv()` with appropriate type conversion and default values:

```python
# Good: Configurable with defaults
YUV_BUFFER_COUNT = int(os.getenv("YUV_BUFFER_COUNT", "20"))
DUAL_CAMERA = bool(int(os.getenv("DUAL", "0")))
CAMERA_ROAD_ID = int(os.getenv("CAMERA_ROAD_ID", "0"))

# Bad: Hard-coded values
YUV_BUFFER_COUNT = 20
DUAL_CAMERA = False
CAMERA_ROAD_ID = 0
```

For platform-specific behavior, prefer hardware abstraction over hard-coded paths:

```python
# Good: Use hardware abstraction
USER_AGENT = f"AGNOSSetup-{HARDWARE.get_os_version()}"

# Bad: Hard-coded file reading
USER_AGENT = f"AGNOSSetup-{open('/VERSION').read().strip()}"
```

This approach allows runtime configuration changes, easier testing with different values, and better separation of configuration from code logic.