---
title: Secure checkout configurations
description: 'When configuring GitHub Actions workflows, pay special attention to
  the checkout action''s configuration to ensure both correctness and security:


  1. In `pull_request_target` workflows, always specify the reference explicitly to
  ensure you''re working with the intended branch:'
repository: hashicorp/terraform
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 45532
---

When configuring GitHub Actions workflows, pay special attention to the checkout action's configuration to ensure both correctness and security:

1. In `pull_request_target` workflows, always specify the reference explicitly to ensure you're working with the intended branch:

```yaml
- name: Checkout code
  uses: actions/checkout@v4
  with:
    ref: ${{ github.head_ref }}
```

2. When your workflow only needs specific files or directories, use sparse-checkout to minimize unnecessary file access and improve security:

```yaml
- name: Checkout specific files
  uses: actions/checkout@v4
  with:
    sparse-checkout: |
      .changes/
      .changie.yaml
```

This practice helps protect against security risks when workflows might have elevated permissions, particularly when running on code from external contributors. Sparse checkouts also improve performance by reducing the amount of data transferred.