---
title: Ensure configuration consistency
description: Maintain consistency across configuration variables to prevent setup
  confusion and deployment issues. Avoid duplicate or conflicting environment variables,
  ensure related configuration values align, and use appropriate defaults for the
  deployment context.
repository: langgenius/dify
label: Configurations
language: Other
comments_count: 3
repository_stars: 114231
---

Maintain consistency across configuration variables to prevent setup confusion and deployment issues. Avoid duplicate or conflicting environment variables, ensure related configuration values align, and use appropriate defaults for the deployment context.

Key practices:
- Align related configuration variables (e.g., passwords, API keys) across different sections
- Avoid duplicate environment variables with different names for the same purpose
- Use context-appropriate defaults (e.g., reasonable token expiry times)
- Ensure configuration variables in example files match their intended usage

Example of inconsistent configuration to avoid:
```bash
# Bad: Misaligned passwords cause login issues
OPENSEARCH_PASSWORD=admin
OPENSEARCH_INITIAL_ADMIN_PASSWORD=Qazwsxedc!@#123

# Bad: Duplicate variables for same purpose
PLUGIN_DAEMON_KEY=lYkiYYT6owG+71oLerGzA7GXCgOT++6ovaezWAjpCjf+Sjc3ZtU+qUEi
PLUGIN_API_KEY=lYkiYYT6owG+71oLerGzA7GXCgOT++6ovaezWAjpCjf+Sjc3ZtU+qUEi
```

This prevents initial setup difficulties and reduces confusion during development and deployment.