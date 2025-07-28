---
title: prefer dynamic configuration sources
description: Use runtime-determined configuration sources instead of hardcoded values
  or static file parsing when more reliable alternatives are available. This improves
  robustness, cross-platform compatibility, and deployment flexibility.
repository: comfyanonymous/ComfyUI
label: Configurations
language: Python
comments_count: 5
repository_stars: 83726
---

Use runtime-determined configuration sources instead of hardcoded values or static file parsing when more reliable alternatives are available. This improves robustness, cross-platform compatibility, and deployment flexibility.

**Examples of preferred approaches:**

- Use `importlib.metadata.version("package-name")` instead of parsing requirements.txt files for version information
- Use `win32api.GetSystemDirectory()` instead of hardcoded paths like `"C:\Windows\System32"`
- Read from runtime environment (like installed packages) rather than static configuration files when both options exist
- Construct paths dynamically using `os.path.join()` instead of hardcoded absolute paths

**Why this matters:**
- Static files can become outdated or contain invalid data (like "max" instead of numbers in cgroup files)
- Hardcoded paths break in different deployment environments or operating systems  
- Runtime sources reflect the actual current state rather than potentially stale configuration files
- Dynamic configuration reduces maintenance burden and improves reliability across different environments

**Implementation:**
```python
# Instead of hardcoded paths:
ICACLS_PATH = r"C:\Windows\System32\icacls.exe"

# Use dynamic system paths:
ICACLS_PATH = os.path.join(win32api.GetSystemDirectory(), "icacls.exe")

# Instead of parsing static files:
with open("requirements.txt", "r") as f:
    version = f.readline().split("=")[-1].strip()

# Use runtime package information:
from importlib.metadata import version
frontend_version = version("comfyui-frontend-package")
```