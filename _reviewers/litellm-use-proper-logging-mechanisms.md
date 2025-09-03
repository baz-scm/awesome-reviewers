---
title: Use proper logging mechanisms
description: Always use the logging library instead of print statements and maintain
  consistent logging patterns throughout the codebase. Print statements should be
  avoided as they bypass proper log level controls, formatting, and routing. Instead,
  use appropriate logging methods like `verbose_logger.info()`, `verbose_logger.debug()`,
  or `verbose_logger.warning()`.
repository: BerriAI/litellm
label: Logging
language: Python
comments_count: 6
repository_stars: 28310
---

Always use the logging library instead of print statements and maintain consistent logging patterns throughout the codebase. Print statements should be avoided as they bypass proper log level controls, formatting, and routing. Instead, use appropriate logging methods like `verbose_logger.info()`, `verbose_logger.debug()`, or `verbose_logger.warning()`.

Centralize logging logic to avoid scattered conditional blocks that can lead to bugs and inconsistent behavior. When implementing logging functionality, encapsulate the logic in dedicated functions or classes rather than duplicating if/else patterns across the codebase.

For logging integrations, use standardized logging objects and interfaces to ensure compatibility and prevent downstream issues.

Example of what to avoid:
```python
print("error", e)  # Don't use print statements
print(file=sys.stderr)  # Even with stderr redirection
```

Example of proper approach:
```python
verbose_logger.info("Processing completed successfully")
verbose_logger.debug("Bedrock AI: make_bedrock_api_request response: %s", redacted_response)
verbose_logger.warning("PostHog API Key not found in environment variables")
```

When dealing with sensitive data, always redact PII and confidential information before logging to prevent security leaks.