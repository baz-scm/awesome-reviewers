---
title: Minimize permission scope
description: When developing browser extensions or applications that use permission
  systems, always follow the principle of least privilege by requesting only the minimum
  permissions necessary for functionality. Broad permissions like `http://*/*` and
  `https://*/*` increase security risks if your code is compromised.
repository: facebook/react
label: Security
language: Json
comments_count: 1
repository_stars: 236926
---

When developing browser extensions or applications that use permission systems, always follow the principle of least privilege by requesting only the minimum permissions necessary for functionality. Broad permissions like `http://*/*` and `https://*/*` increase security risks if your code is compromised.

Instead of:
```json
"permissions": [
  "scripting",
  "storage",
  "tabs",
  "http://*/*",
  "https://*/*"
]
```

Consider more specific scopes when possible:
```json
"permissions": [
  "scripting",
  "storage",
  "tabs"
],
"host_permissions": [
  "https://specific-domain.com/*"
]
```

Only request broad URL permissions when absolutely necessary for the application's core functionality, and document why such permissions are required. Regularly review permissions as APIs evolve (e.g., Manifest v3 changes) to ensure you're not requesting unnecessary access.