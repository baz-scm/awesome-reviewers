---
title: Never commit secrets
description: Private cryptographic keys, certificates with private keys, and other
  secrets must never be committed to source code repositories, even in test or spec
  files. This is a critical security vulnerability that could lead to unauthorized
  access, impersonation, or system compromise.
repository: chef/chef
label: Security
language: Other
comments_count: 6
repository_stars: 7860
---

Private cryptographic keys, certificates with private keys, and other secrets must never be committed to source code repositories, even in test or spec files. This is a critical security vulnerability that could lead to unauthorized access, impersonation, or system compromise.

When finding private keys in code like this:
```
-----BEGIN CERTIFICATE-----
MIIDRDCCAiygAwIBAgIBAzANBgkqhkiG9w0BAQsFADA4MQswCQYDVQQGEwJVUzEQ
...certificate content...
-----END CERTIFICATE-----
-----BEGIN RSA PRIVATE KEY-----
... private key content ...
```

Take immediate action:
1. Revoke the exposed keys to invalidate them
2. Generate new keys/credentials to replace the compromised ones
3. Remove all secrets from the codebase
4. Implement secure secret management

Security best practices for handling secrets:
- Use environment variables for sensitive information
- Implement dedicated secret management tools (HashiCorp Vault, AWS Secrets Manager, etc.)
- For test environments, use clearly marked dummy values or mock security components
- Add secret detection to CI/CD pipelines and pre-commit hooks
- Include secret files in .gitignore to prevent accidental commits

Properly managing cryptographic material ensures your systems remain secure and prevents costly security incidents resulting from leaked credentials.
