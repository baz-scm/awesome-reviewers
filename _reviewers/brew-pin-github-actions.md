---
title: Pin GitHub actions
description: Always pin GitHub Actions to specific commit hashes rather than version
  tags (like @v4). Using version tags is a security vulnerability as the tag owner
  could change what commit the tag points to, potentially introducing malicious code
  into your workflow. This is a common supply chain security best practice.
repository: Homebrew/brew
label: Security
language: Yaml
comments_count: 2
repository_stars: 44168
---

Always pin GitHub Actions to specific commit hashes rather than version tags (like @v4). Using version tags is a security vulnerability as the tag owner could change what commit the tag points to, potentially introducing malicious code into your workflow. This is a common supply chain security best practice.

Example:
```yaml
# INSECURE - Using version tag
steps:
  - name: Checkout Homebrew
    uses: actions/checkout@v4

# SECURE - Using commit hash
steps:
  - name: Checkout Homebrew
    uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4
```

Including the version as a comment after the hash helps with maintainability while preserving security.