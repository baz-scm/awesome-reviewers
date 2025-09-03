---
title: Use secure credential storage
description: Avoid storing sensitive credentials like usernames and passwords in environment
  variables. Instead, use dedicated secrets management systems such as HashiCorp Vault,
  AWS Secrets Manager, Azure Key Vault, or your CI/CD platform's built-in secrets
  management.
repository: SigNoz/signoz
label: Security
language: TypeScript
comments_count: 1
repository_stars: 23369
---

Avoid storing sensitive credentials like usernames and passwords in environment variables. Instead, use dedicated secrets management systems such as HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, or your CI/CD platform's built-in secrets management.

Environment variables can be easily exposed through process listings, logs, or configuration dumps, making them unsuitable for sensitive data. Secrets management systems provide better security through encryption at rest, access controls, audit logging, and automatic rotation capabilities.

Example of problematic pattern:
```typescript
// Avoid: Reading sensitive credentials from environment variables
const username = process.env.SIGNOZ_E2E_USERNAME;
const password = process.env.SIGNOZ_E2E_PASSWORD;
```

Instead, integrate with your organization's secrets management solution or use your CI/CD platform's secure secrets storage for accessing sensitive credentials during automated processes.