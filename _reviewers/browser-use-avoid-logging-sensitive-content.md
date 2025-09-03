---
title: Avoid logging sensitive content
description: 'Be cautious about what data gets included in log messages to prevent
  security risks and performance issues. Before logging file contents or user data,
  consider whether it could contain:'
repository: browser-use/browser-use
label: Logging
language: Python
comments_count: 2
repository_stars: 69139
---

Be cautious about what data gets included in log messages to prevent security risks and performance issues. Before logging file contents or user data, consider whether it could contain:

- Binary data (images, PDFs, executables)
- Personally identifiable information (PII)
- Extremely large content that could overwhelm logs or consume excessive memory
- Sensitive configuration or authentication data

Instead of logging full content, log metadata like file names, sizes, types, or character counts. Use appropriate log levels - consolidate related error information into a single error log rather than splitting across multiple log statements.

Example of what to avoid:
```python
# Bad - logs potentially sensitive/large content
file_content = file_system.read_file(file_name)
logger.info(f'Read file contents: {file_content}')

# Bad - splits error information
logger.info("error during llm invocation")
logger.error(e)
```

Example of better approach:
```python
# Good - logs metadata only
file_content = file_system.read_file(file_name)
logger.info(f'Read file {file_name} ({len(file_content)} characters)')

# Good - consolidated error logging
logger.error(f"Error during LLM invocation: {e}")
```