---
title: Consistent naming standards
description: Follow standard Python naming conventions consistently throughout code
  and documentation. Use underscores instead of hyphens in variable and parameter
  names (e.g., `proxies_config` not `proxies-config`). Maintain consistent capitalization
  of technical terms across all documentation. When working with file paths in code
  examples, use platform-agnostic...
repository: boto/boto3
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 9417
---

Follow standard Python naming conventions consistently throughout code and documentation. Use underscores instead of hyphens in variable and parameter names (e.g., `proxies_config` not `proxies-config`). Maintain consistent capitalization of technical terms across all documentation. When working with file paths in code examples, use platform-agnostic formats that work across all operating systems:

```python
# Good
filename = 'file.txt'

# Avoid (Windows-specific)
filename = 'C:\file.txt'
```

This consistency improves code readability, ensures cross-platform compatibility, and helps maintain a professional, unified appearance across the codebase and documentation.