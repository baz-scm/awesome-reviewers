---
title: Document security implications
description: When writing documentation that involves handling sensitive data or security-related
  operations, always include explicit warnings about security implications and provide
  references to security best practices. Users may not be aware of default security
  behaviors that could expose sensitive information.
repository: volcano-sh/volcano
label: Security
language: Markdown
comments_count: 1
repository_stars: 4899
---

When writing documentation that involves handling sensitive data or security-related operations, always include explicit warnings about security implications and provide references to security best practices. Users may not be aware of default security behaviors that could expose sensitive information.

For example, when documenting the creation of Kubernetes Secrets, include a warning that Secrets are unencrypted by default:

```bash
kubectl create secret generic ufm-credentials \
  --from-literal=username='your-ufm-username' \
  --from-literal=password='your-ufm-password' \
  -n volcano-system
```

> Warning: Secrets are still unencrypted by default. If users need to encrypt Secrets, please refer to: https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/

This practice helps users make informed security decisions and prevents accidental exposure of sensitive data due to lack of awareness about default security configurations.