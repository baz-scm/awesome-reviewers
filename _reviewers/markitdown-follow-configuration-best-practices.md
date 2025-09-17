---
title: Follow configuration best practices
description: Always adhere to official guidelines and proper validation when setting
  up configurations, whether for dependencies, file formats, or environment setup.
  This prevents subtle issues that can cause tests to pass incorrectly or create environment
  conflicts.
repository: microsoft/markitdown
label: Configurations
language: Other
comments_count: 2
repository_stars: 76602
---

Always adhere to official guidelines and proper validation when setting up configurations, whether for dependencies, file formats, or environment setup. This prevents subtle issues that can cause tests to pass incorrectly or create environment conflicts.

For dependency installation, use the recommended method from official documentation rather than generic approaches:
```makefile
# Instead of:
install:
	pip install hatch

# Use the recommended approach:
install:
	pipx install hatch
```

For file configurations, validate that files have the correct format and MIME type, not just the right extension. A .doc file should have MIME type `application/msword`, not `application/octet-stream`. Simply renaming a .docx file to .doc doesn't change its underlying format and can lead to false test results.

This practice ensures reliable, conflict-free environments and prevents configuration-related bugs from propagating through your system.