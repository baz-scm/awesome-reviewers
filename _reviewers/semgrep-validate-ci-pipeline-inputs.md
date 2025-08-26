---
title: Validate CI pipeline inputs
description: Always validate and sanitize dynamic inputs in CI/CD pipelines before
  using them in URLs, file operations, or other system interactions. This includes
  environment variables, repository names, file paths, and user-provided parameters
  that could contain special characters, spaces, or unexpected formats.
repository: semgrep/semgrep
label: CI/CD
language: Python
comments_count: 2
repository_stars: 12598
---

Always validate and sanitize dynamic inputs in CI/CD pipelines before using them in URLs, file operations, or other system interactions. This includes environment variables, repository names, file paths, and user-provided parameters that could contain special characters, spaces, or unexpected formats.

Key validation practices:
- Sanitize repository names and deployment names before URL construction to prevent broken links
- Check file existence and handle renamed/deleted files in baseline comparisons
- "Slug-ify" user inputs that become part of URLs to handle spaces and special characters
- Validate environment variables before incorporating them into system operations

Example of problematic URL construction:
```python
# Problematic - can create broken URLs like /orgs/semgrep/findings?repo=semgrep/semgrep/semgrep
f"https://semgrep.dev/orgs/{scan_handler.deployment_name}/findings?repo={scan_handler.deployment_name}/{metadata.repo_display_name}"

# Better - validate and sanitize inputs
f"https://semgrep.dev/orgs/{scan_handler.deployment_name}/findings?repo={sanitized_repo_name}"
```

This prevents CI pipeline failures, broken reporting links, and unexpected behavior when processing dynamic content or state changes between pipeline runs.