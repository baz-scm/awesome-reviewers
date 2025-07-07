---
title: Maintain package verification
description: Always keep signature verification enabled in package managers, even
  in development environments, Docker containers, or when facing initialization challenges.
  Disabling signature verification creates a significant security vulnerability by
  allowing potentially compromised or malicious packages to be installed.
repository: tensorflow/tensorflow
label: Security
language: Other
comments_count: 1
repository_stars: 190625
---

Always keep signature verification enabled in package managers, even in development environments, Docker containers, or when facing initialization challenges. Disabling signature verification creates a significant security vulnerability by allowing potentially compromised or malicious packages to be installed.

**Why this matters**: Package signature verification is a critical defense against supply chain attacks. Even temporary disabling for convenience can expose systems to compromise.

**Example - Do not do this**:
```dockerfile
# Disable signature checking on pacman because we cannot initialize the keyring
RUN pacman-key --init && pacman -Sy --noconfirm --disable-download-timeout
```

**Instead do this**:
```dockerfile
# Initialize keyring properly to maintain signature checking
RUN pacman-key --init && pacman-key --populate && pacman -Sy --noconfirm --disable-download-timeout
```

When facing difficulties with package signature verification, research the proper initialization method rather than disabling the security feature.