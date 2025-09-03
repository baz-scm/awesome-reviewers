---
title: Document log level options
description: When documenting logging configuration parameters, always provide the
  complete list of available log level options and use consistent naming conventions.
  This ensures developers understand all available choices and prevents confusion
  from incomplete documentation.
repository: langflow-ai/langflow
label: Logging
language: Other
comments_count: 2
repository_stars: 111046
---

When documenting logging configuration parameters, always provide the complete list of available log level options and use consistent naming conventions. This ensures developers understand all available choices and prevents confusion from incomplete documentation.

Log levels should be documented in lowercase format consistently across all interfaces (CLI, environment variables, configuration files). When a parameter accepts log level values, explicitly list all valid options rather than showing only the default.

Example:
```
| `--log-level` | `error` | String | Set the logging level. Possible values: `debug`, `info`, `warning`, `error`, `critical`. |
```

This practice helps developers make informed decisions about logging configuration and ensures consistency across different parts of the system documentation.