---
title: avoid unnecessary workflow restrictions
description: Remove unnecessary approval gates, custom tokens, and restrictive conditions
  in CI/CD workflows when existing security measures are sufficient. Over-restrictive
  workflows create friction without meaningful security benefits.
repository: TanStack/router
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 11590
---

Remove unnecessary approval gates, custom tokens, and restrictive conditions in CI/CD workflows when existing security measures are sufficient. Over-restrictive workflows create friction without meaningful security benefits.

For example, avoid adding approval requirements when contributor workflows already require approval:
```yaml
jobs:
  preview:
    name: Preview
    # Remove unnecessary approval check
    # if: github.event.review.state == 'APPROVED'
```

Similarly, use built-in tokens when appropriate instead of custom secrets:
```yaml
- uses: actions/labeler@v4.3.0
  with:
    repo-token: ${{ secrets.GITHUB_TOKEN }}  # Use built-in token
```

Evaluate each workflow condition to ensure it adds genuine security value rather than just creating additional steps.