---
title: Use standard example credentials
description: 'When including API keys, access tokens, or other credentials in documentation,
  examples, or test code, always use clearly marked standard formats that won''t trigger
  security scanners or be mistaken for real credentials. '
repository: boto/boto3
label: Security
language: Other
comments_count: 1
repository_stars: 9417
---

When including API keys, access tokens, or other credentials in documentation, examples, or test code, always use clearly marked standard formats that won't trigger security scanners or be mistaken for real credentials. 

For AWS resources specifically, use the official example format (e.g., `AKIAIOSFODNN7EXAMPLE` for access keys) rather than realistic-looking keys like `APKBJCAOBHD36274ZIZA`.

```python
# Instead of this:
key_id = 'APKBJCAOBHD36274ZIZA'

# Use this:
key_id = 'AKIAIOSFODNN7EXAMPLE'
```

This practice prevents accidental credential leakage, avoids false positives in security scans like `git-secrets`, and establishes consistent patterns across your codebase. Even example credentials that aren't valid can still trigger security alerts or create confusion if they appear to be real.