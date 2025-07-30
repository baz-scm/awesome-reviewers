---
title: Document credential formats
description: When documenting security-sensitive parameters such as private keys,
  certificates, API tokens, or other authentication credentials, always specify the
  expected format including any required headers, footers, and structural elements.
  This prevents configuration errors that could lead to authentication failures or
  security vulnerabilities.
repository: Unstructured-IO/unstructured
label: Security
language: Other
comments_count: 1
repository_stars: 12117
---

When documenting security-sensitive parameters such as private keys, certificates, API tokens, or other authentication credentials, always specify the expected format including any required headers, footers, and structural elements. This prevents configuration errors that could lead to authentication failures or security vulnerabilities.

For example, when documenting a private key parameter, clarify the format:

```
- ``Private Key (PEM)`` (*required*): Input the Private Key associated with the Consumer Key. 
  The key should begin with -----BEGIN RSA PRIVATE KEY----- and end with -----END RSA PRIVATE KEY-----.
```

This practice helps users correctly configure security credentials and reduces the risk of authentication issues or security misconfigurations that could compromise system security.