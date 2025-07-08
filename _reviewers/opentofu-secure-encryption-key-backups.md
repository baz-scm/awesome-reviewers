---
title: Secure encryption key backups
description: Always implement proper encryption key management procedures, including
  secure backups of encryption keys before enabling encryption features. Without proper
  key backups, encrypted data can become permanently inaccessible, creating security
  and operational risks.
repository: opentofu/opentofu
label: Security
language: Other
comments_count: 1
repository_stars: 25901
---

Always implement proper encryption key management procedures, including secure backups of encryption keys before enabling encryption features. Without proper key backups, encrypted data can become permanently inaccessible, creating security and operational risks.

When implementing encryption:
- Create and test a disaster recovery plan
- Make temporary backups of unencrypted data before encryption
- Establish secure storage for encryption keys with redundant backups
- Document key rotation schedules and procedures
- Consider using key management systems for sensitive environments

```hcl
# Before enabling encryption in configuration
# 1. Back up your unencrypted state
$ cp terraform.tfstate terraform.tfstate.backup

# 2. Ensure encryption keys are securely backed up
# 3. Then enable encryption in your configuration
terraform {
  # Configuration with encryption enabled
  state_encryption {
    # Your encryption configuration
    # ...
  }
}

# Remember: Once encryption is enabled, access to data requires the correct key
```

Failure to maintain access to encryption keys can result in permanent data loss, as encrypted data cannot be recovered without the correct key.