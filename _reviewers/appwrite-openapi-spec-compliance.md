---
title: OpenAPI spec compliance
description: 'Ensure all API definitions strictly follow OpenAPI specification standards
  to maintain compatibility with tooling and clients. This includes:


  1. Match default values with their defined types:'
repository: appwrite/appwrite
label: API
language: Json
comments_count: 3
repository_stars: 51959
---

Ensure all API definitions strictly follow OpenAPI specification standards to maintain compatibility with tooling and clients. This includes:

1. Match default values with their defined types:
```diff
"data": {
  "type": "object",
  "description": "Document data as JSON object.",
-  "default": [],
+  "default": {},
}
```

2. Place custom properties under vendor extensions (x-prefix):
```diff
- "methods": [
+ "x-appwrite-methods": [
  {
    "name": "createDocument",
    ...
  }
]
```

3. Use proper variable syntax for URL templates:
```diff
- "url": "https://<REGION>.cloud.appwrite.io/v1"
+ "url": "https://{region}.cloud.appwrite.io/v1",
+ "variables": {
+   "region": {
+     "description": "Regional subdomain (e.g., us-east-1)",
+     "default": "us-east-1"
+   }
+ }
```

Maintaining specification compliance ensures API documentation is accurate, enables proper code generation, and provides a consistent developer experience.