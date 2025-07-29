---
title: Secure GPG verification
description: When downloading and verifying packages using GPG signatures, follow
  secure practices to ensure authenticity and prevent security vulnerabilities. Use
  hardcoded GPG keys rather than dynamic ones, employ reliable keyservers, set proper
  GNUPGHOME environment, and clean up GPG processes after verification.
repository: apache/kafka
label: Security
language: Dockerfile
comments_count: 1
repository_stars: 30575
---

When downloading and verifying packages using GPG signatures, follow secure practices to ensure authenticity and prevent security vulnerabilities. Use hardcoded GPG keys rather than dynamic ones, employ reliable keyservers, set proper GNUPGHOME environment, and clean up GPG processes after verification.

Key practices include:
- Hardcode GPG_KEY values as environment variables for transparency
- Use only reliable, maintained keyservers (e.g., hkp://keys.openpgp.org, keyserver.ubuntu.com)
- Set GNUPGHOME to isolate GPG operations
- Clean up GPG processes with `gpgconf --kill all` after verification
- Download from HTTPS sources when possible

Example implementation:
```dockerfile
ENV GPG_KEY CF9500821E9557AEB04E026C05EEA67F87749E61

RUN set -eux ; \
    for server in hkp://keys.openpgp.org keyserver.ubuntu.com ; do \
      gpg --batch --keyserver "$server" --recv-keys "$GPG_KEY" && break || : ; \
    done && \
    wget -nv -O package.tgz "$package_url"; \
    wget -nv -O package.tgz.asc "$package_url.asc"; \
    gpg --batch --verify package.tgz.asc package.tgz; \
    gpgconf --kill all
```

This approach follows Docker official images guidelines and established practices from projects like Apache Flink, ensuring package integrity while maintaining security best practices.