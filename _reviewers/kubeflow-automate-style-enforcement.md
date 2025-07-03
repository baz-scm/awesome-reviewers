---
title: Automate style enforcement
description: 'Configure your development environment to automatically enforce code
  style standards rather than relying on manual checks during code review. This includes:'
repository: kubeflow/kubeflow
label: Code Style
language: Yaml
comments_count: 2
repository_stars: 15064
---

Configure your development environment to automatically enforce code style standards rather than relying on manual checks during code review. This includes:

1. Use modern, actively maintained linting tools instead of deprecated ones (e.g., replace tslint with eslint)
2. Configure your IDE to automatically apply formatting rules, such as adding newlines at end of files

Example IDE configuration for VSCode (settings.json):
```json
{
  "files.insertFinalNewline": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

This approach reduces style-related comments in code reviews, ensures consistency across the codebase, and allows reviewers to focus on more substantive issues.
