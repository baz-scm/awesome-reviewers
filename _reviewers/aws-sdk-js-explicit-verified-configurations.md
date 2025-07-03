---
title: Explicit verified configurations
description: Always specify configuration values explicitly and verify their accuracy
  against official documentation or tests. This applies to region configurations,
  API settings, and credential management. Avoid mutations of global configuration
  objects, and instead set values explicitly when defined by service APIs.
repository: aws/aws-sdk-js
label: Configurations
language: Json
comments_count: 3
repository_stars: 7628
---

Always specify configuration values explicitly and verify their accuracy against official documentation or tests. This applies to region configurations, API settings, and credential management. Avoid mutations of global configuration objects, and instead set values explicitly when defined by service APIs.

Example:
```json
// GOOD: Explicitly verified region configuration
"us-iso-*/iam": {
  "endpoint": "{service}.us-iso-east-1.c2s.ic.gov",
  "globalEndpoint": true,
  "signingRegion": "us-iso-east-1"  // Verified against Endpoints 2.0 tests
}

// BAD: Incorrect or unverified configuration
"us-iso-*/iam": {
  "endpoint": "{service}.us-iso-east-1.c2s.ic.gov",
  "globalEndpoint": true,
  "signingRegion": "us-east-1"  // Incorrect region
}
```

For credential configurations, always use resolved credentials when available rather than relying on automatic refresh mechanisms that may cause performance issues.
