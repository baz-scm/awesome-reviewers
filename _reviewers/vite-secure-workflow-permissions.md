---
title: Secure workflow permissions
description: Define explicit and minimal permissions in GitHub Actions workflows to
  ensure proper operation while maintaining security. Workflows should only have permissions
  necessary for their intended tasks, and permission checks should occur early in
  the workflow to prevent unnecessary actions.
repository: vitejs/vite
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 74031
---

Define explicit and minimal permissions in GitHub Actions workflows to ensure proper operation while maintaining security. Workflows should only have permissions necessary for their intended tasks, and permission checks should occur early in the workflow to prevent unnecessary actions.

For workflows that modify resources:
- Add specific permission scopes (e.g., `issues: write` for workflows that close issues)
- Use empty `permissions: {}` as a default and add only what's needed
- Place permission validation at the top of workflows to fail fast

Example:
```yaml
name: Issue Management Workflow

# Start with empty permissions
permissions: {}

jobs:
  manage-issues:
    runs-on: ubuntu-latest
    # Add only required permissions
    permissions:
      issues: write
    
    steps:
      # Check user permissions first before proceeding
      - name: Check User Permissions
        uses: actions/github-script@v7
        with:
          script: |
            // Verify user has appropriate permissions
            if (!context.payload.sender.permissions.write) {
              core.setFailed('User does not have write permissions')
              return
            }
            
      # Remaining steps only execute if permissions check passes
      - name: Close stale issues
        # ...
```

This approach minimizes security risks, prevents workflow failures due to permission issues, and follows the principle of least privilege.