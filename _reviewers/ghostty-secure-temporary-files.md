---
title: Secure temporary files
description: Always use `mktemp` instead of manually constructing temporary file paths
  with random values. Manually constructed paths with elements like `$RANDOM` or timestamp
  values can be vulnerable to race conditions, predictability issues, and permission
  problems, potentially leading to security exploits.
repository: ghostty-org/ghostty
label: Security
language: Other
comments_count: 1
repository_stars: 32864
---

Always use `mktemp` instead of manually constructing temporary file paths with random values. Manually constructed paths with elements like `$RANDOM` or timestamp values can be vulnerable to race conditions, predictability issues, and permission problems, potentially leading to security exploits.

**Instead of:**
```bash
cpath="/tmp/ghostty-ssh-$USER-$RANDOM-$(date +%s)"
```

**Use:**
```bash
cpath=$(mktemp -d /tmp/ghostty-ssh-XXXXXX)
# or for a file
cpath=$(mktemp /tmp/ghostty-ssh-XXXXXX)
```

The `mktemp` utility creates unique temporary files/directories safely, sets appropriate permissions, and handles race conditions properly. This prevents potential security vulnerabilities like file-based race conditions, symbolic link attacks, and information disclosure that could occur with manually constructed paths.