---
title: Azure encryption property names
description: When configuring encryption settings for Azure resources in ARM templates,
  always use the correct property names as documented in the Azure API specifications.
  Specifically for Azure Compute disks, use `enableDoubleEncryption` instead of `doubleEncryptionEnabled`
  to configure double encryption. Using incorrect property names can result in security...
repository: bridgecrewio/checkov
label: Security
language: Json
comments_count: 2
repository_stars: 7667
---

When configuring encryption settings for Azure resources in ARM templates, always use the correct property names as documented in the Azure API specifications. Specifically for Azure Compute disks, use `enableDoubleEncryption` instead of `doubleEncryptionEnabled` to configure double encryption. Using incorrect property names can result in security configurations silently failing to be applied, potentially leaving resources vulnerable.

Example:
```json
// INCORRECT
{
  "properties": {
    "doubleEncryptionEnabled": true  // Wrong property name
  }
}

// CORRECT
{
  "properties": {
    "enableDoubleEncryption": true  // Correct property name
  }
}
```