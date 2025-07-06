---
title: "Use bot identity"
description: "When configuring Git operations in GitHub Actions workflows, especially for automated commits, use the GitHub Actions bot identity instead of personal user accounts. This clearly distinguishes automated actions from manual ones, provides better audit trails, and avoids personal attribution for system-generated changes."
repository: "fastify/fastify"
label: "CI/CD"
language: "Yaml"
comments_count: 2
repository_stars: 34000
---

When configuring Git operations in GitHub Actions workflows, especially for automated commits, use the GitHub Actions bot identity instead of personal user accounts. This clearly distinguishes automated actions from manual ones, provides better audit trails, and avoids personal attribution for system-generated changes.

**Implementation:**
```yaml
- name: Git Config
  run: |
    git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
    git config --global user.name "github-actions[bot]"
```

This approach ensures that commit history properly reflects which changes were made through automation versus direct developer intervention, making repository history more transparent and accurate. It also prevents confusion that might arise when commits appear to come from individuals but are actually from automated processes.