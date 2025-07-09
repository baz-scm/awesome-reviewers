---
title: Prevent workflow recursion
description: 'Control GitHub Actions workflow execution to avoid infinite loops and
  unnecessary builds. Implement these practices:


  1. **Add `paths-ignore` filters** for generated files that might trigger the workflow
  again:'
repository: elie222/inbox-zero
label: CI/CD
language: Yaml
comments_count: 4
repository_stars: 8267
---

Control GitHub Actions workflow execution to avoid infinite loops and unnecessary builds. Implement these practices:

1. **Add `paths-ignore` filters** for generated files that might trigger the workflow again:

```yaml
on:
  push:
    branches: ["main"]
    paths-ignore:
      - version.txt  # Skip when only version files change
```

2. **Explicitly specify branch references** when checking out code to ensure the correct version is processed:

```yaml
- name: Checkout code
  uses: actions/checkout@v4
  with:
    ref: main  # Explicitly reference the target branch
    fetch-depth: 0
```

3. **Target the correct branch** when pushing changes to avoid misdirected commits:

```yaml
- name: Push changes
  uses: ad-m/github-push-action@master
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    branch: trails  # Explicitly specify the target branch
```

4. **Restrict event triggers** to only required events to prevent premature actions:

```yaml
on:
  push:
    branches: [ "main" ]
  # pull_request:  # Remove if not needed for publishing operations
  #   branches: [ "main" ]
```

These practices ensure your workflows run only when needed and operate on the correct code, preventing wasteful CI resources and confusing version history.