---
title: Pin actions securely
description: Always pin GitHub Actions to specific commit hashes rather than version
  tags to prevent supply chain attacks and ensure build reproducibility. This practice
  ensures that your workflow remains stable and secure even if the action's version
  tag is compromised or modified.
repository: n8n-io/n8n
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 122978
---

Always pin GitHub Actions to specific commit hashes rather than version tags to prevent supply chain attacks and ensure build reproducibility. This practice ensures that your workflow remains stable and secure even if the action's version tag is compromised or modified.

For example, use:
```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
- uses: docker/setup-qemu-action@29109295f81e9208d7d86ff1c6c12d2833863392 # v3.6.0
```

Additionally:

1. Use appropriate authentication tokens with minimal required permissions for external operations. Default GITHUB_TOKEN lacks permissions for cross-repository operations, so use dedicated tokens for these scenarios:
```yaml
- name: Generate GitHub App Token
  id: generate_token
  uses: actions/create-github-app-token@v2
  with:
    app-id: ${{ secrets.APP_ID }}
    private-key: ${{ secrets.PRIVATE_KEY }}

- name: Checkout External Repository
  uses: actions/checkout@v4
  with:
    repository: org/external-repo
    token: ${{ steps.generate_token.outputs.token }}
```

2. Leverage reusable actions for common workflows to ensure consistency and reduce maintenance overhead:
```yaml
- name: Setup Environment and Build Project
  uses: ./.github/actions/setup-and-build
  with:
    node-version: 20.x
    enable-caching: true
```