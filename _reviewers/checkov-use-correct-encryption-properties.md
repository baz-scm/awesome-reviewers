---
title: Use correct encryption properties
description: When configuring security features in Azure ARM templates, always use
  the correct property names as specified in the Azure documentation. For double encryption
  of Azure Compute disks, use "enableDoubleEncryption" rather than "doubleEncryptionEnabled".
  Using incorrect property names may result in security features not being properly
  applied, potentially...
repository: bridgecrewio/checkov
label: Security
language: Json
comments_count: 2
repository_stars: 7668
---

When configuring security features in Azure ARM templates, always use the correct property names as specified in the Azure documentation. For double encryption of Azure Compute disks, use "enableDoubleEncryption" rather than "doubleEncryptionEnabled". Using incorrect property names may result in security features not being properly applied, potentially leaving resources vulnerable even when you intended to secure them.

```json
// INCORRECT
"properties": {
  "doubleEncryptionEnabled": true
}

// CORRECT
"properties": {
  "enableDoubleEncryption": true
}
```