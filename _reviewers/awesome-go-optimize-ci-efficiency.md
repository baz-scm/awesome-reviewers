---
title: optimize CI efficiency
description: Optimize CI/CD pipelines by minimizing resource usage and avoiding unnecessary
  operations. Use lightweight package alternatives when possible (e.g., `vim-nox`
  instead of `vim` for text processing), implement conditional execution to run steps
  only when relevant files change, and leverage automatic dependency resolution instead
  of manual listings.
repository: avelino/awesome-go
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 151435
---

Optimize CI/CD pipelines by minimizing resource usage and avoiding unnecessary operations. Use lightweight package alternatives when possible (e.g., `vim-nox` instead of `vim` for text processing), implement conditional execution to run steps only when relevant files change, and leverage automatic dependency resolution instead of manual listings.

For package optimization, prefer minimal variants:
```yaml
- name: Install Vim
  run: apt-get update; apt-get install -y vim-nox;
```

For conditional execution, use file change detection:
```yaml
- name: Verify Changed Files
  uses: tj-actions/verify-changed-files@v16
  with:
    files_ignore: |
      *.md
```

For dependency management, use automatic resolution:
```yaml
- name: Get dependencies
  run: go get -t -v ./...
```

This approach reduces CI execution time, minimizes resource consumption, and prevents unnecessary workflow runs while maintaining functionality. It's particularly important for repositories with frequent contributions that don't affect core functionality.