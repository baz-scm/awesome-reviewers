---
title: Secure file uploads
description: Always implement and maintain robust scanning mechanisms for user-uploaded
  files to prevent malware distribution. When modifying infrastructure or services
  related to file handling, ensure alternative security controls are in place before
  removing existing protections.
repository: appwrite/appwrite
label: Security
language: Yaml
comments_count: 1
repository_stars: 51959
---

Always implement and maintain robust scanning mechanisms for user-uploaded files to prevent malware distribution. When modifying infrastructure or services related to file handling, ensure alternative security controls are in place before removing existing protections.

Examples:
1. When removing an antivirus service like ClamAV:
```yaml
# Incorrect - commenting out without alternative
services:
  appwrite:
    depends_on:
      - mariadb
      - redis
#      - clamav  # Security risk: Removed without replacement

# Correct - either keep the service or document alternative
services:
  appwrite:
    depends_on:
      - mariadb
      - redis
      - clamav  # Maintain file scanning
    # Alternative: Implement cloud-based scanning solution as documented in security.md
```

2. Ensure application logic handles scanning failure gracefully:
```php
// Verify uploads are always scanned before processing
if (!$scanService->isAvailable() && !$alternativeScanner->isAvailable()) {
    throw new SecurityException('No file scanning service available');
}
```