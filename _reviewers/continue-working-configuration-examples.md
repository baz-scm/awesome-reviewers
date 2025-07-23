---
title: Working configuration examples
description: Configuration examples should be complete, accurate, and ready to use
  without modification. This applies to both code snippets and configuration file
  examples.
repository: continuedev/continue
label: Configurations
language: Markdown
comments_count: 4
repository_stars: 27819
---

Configuration examples should be complete, accurate, and ready to use without modification. This applies to both code snippets and configuration file examples.

For code examples that use configuration:
- Include all necessary imports (e.g., `import os` when using `os.environ`)
- Ensure variables referenced are properly defined
- Verify that referenced configuration values are current and functional

For configuration file examples:
- Use explicit, platform-agnostic terminology (use "autocomplete hints" rather than "IntelliSense")
- Document all required parameters and their defaults
- Clearly explain behavior differences resulting from configuration changes

Example of good practice:
```python
# Complete example with imports
import os

# Configure Bearer authorization
configuration = openapi_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)
```

Example of good configuration documentation:
```json
{
  "name": "commit",
  "description": "Generate a commit message for staged changes",
  "params": { "includeUnstaged": true }
}
```
With explanation: "If `includeUnstaged` is set to true, then unstaged changes are also included in the prompt, otherwise only staged changes are included."