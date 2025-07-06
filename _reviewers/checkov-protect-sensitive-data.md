---
title: Protect sensitive data
description: Never log, display, or store sensitive information like passwords, tokens,
  or secrets in clear text. This creates significant security vulnerabilities that
  could lead to unauthorized access and data breaches.
repository: bridgecrewio/checkov
label: Security
language: Python
comments_count: 16
repository_stars: 7668
---

Never log, display, or store sensitive information like passwords, tokens, or secrets in clear text. This creates significant security vulnerabilities that could lead to unauthorized access and data breaches.

When working with sensitive data:
1. Mask or hash sensitive values before logging
2. Use secure logging frameworks that automatically redact sensitive data
3. Implement proper encryption for data at rest and in transit
4. Use dedicated secure storage solutions for secrets

Example of vulnerable code:
```python
# Insecure - logs sensitive data in clear text
logging.info(f"cloning {git_url} to {clone_dir}")
print(f'attempting to load module {module_params.module_source} via git loader')
```

Secure alternative:
```python
# Secure - masks sensitive information
safe_url = re.sub(r'(https?://)([^:]+)(:.+@|@)(.*)', r'\1\2@\4', git_url)
logging.info(f"cloning {safe_url} to {clone_dir}")

# For debugging, avoid logging sensitive parameters directly
logging.info(f"attempting to load module via git loader")
```