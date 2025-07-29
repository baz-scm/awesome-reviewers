---
title: Network request configuration
description: When implementing or documenting network functionality, ensure proper
  configuration options are provided and compatibility across different environments
  is considered. Network requests should have configurable timeouts and work reliably
  across platform variations.
repository: python-poetry/poetry
label: Networking
language: Markdown
comments_count: 2
repository_stars: 33496
---

When implementing or documenting network functionality, ensure proper configuration options are provided and compatibility across different environments is considered. Network requests should have configurable timeouts and work reliably across platform variations.

For timeout configuration, document default values and provide environment variables for customization:
```bash
# Default timeout is 15 seconds, similar to pip
# Use POETRY_REQUESTS_TIMEOUT to customize
export POETRY_REQUESTS_TIMEOUT=30
```

For cross-platform network requests, include platform-specific parameters when necessary:
```powershell
# Windows PowerShell 5.1 compatibility
(Invoke-WebRequest -Uri https://example.com/script.py -UseBasicParsing).Content | python
```

This ensures network operations are both configurable for different use cases and compatible across the environments where users will actually run the code. Always test network functionality on the target platforms and document any platform-specific requirements or parameters needed for reliable operation.