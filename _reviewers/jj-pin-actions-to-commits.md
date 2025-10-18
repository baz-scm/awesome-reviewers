---
title: Pin actions to commits
description: Use specific commit hashes instead of version tags when referencing GitHub
  Actions in CI/CD workflows. Version tags can be moved or updated, potentially introducing
  security vulnerabilities or breaking changes, while commit hashes are immutable
  and provide reproducible builds.
repository: jj-vcs/jj
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 21171
---

Use specific commit hashes instead of version tags when referencing GitHub Actions in CI/CD workflows. Version tags can be moved or updated, potentially introducing security vulnerabilities or breaking changes, while commit hashes are immutable and provide reproducible builds.

Replace version tags like `@v4` or `@v3` with the full commit hash:

```yaml
# Instead of:
- uses: actions/checkout@v4
- uses: DeterminateSystems/determinate-nix-action@v3

# Use:
- uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8
- uses: DeterminateSystems/determinate-nix-action@b7303d63f88908d15f0bcb207e60b3a0ea7f1712
```

This practice enhances security by preventing supply chain attacks where malicious actors could update the code behind a version tag, and ensures reproducible builds by guaranteeing the exact same action code runs every time.