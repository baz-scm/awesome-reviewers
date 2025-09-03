---
title: Dependency version management
description: Use semantic versioning ranges for dependencies instead of "latest" or
  overly broad ranges. Avoid "latest" as it can cause caching issues during updates.
  Maintain minimum required version semantics to ensure compatibility - if your code
  requires features from version 4.4, specify "^4.4" rather than "^4" to prevent runtime
  errors when using tools like pnpm...
repository: lobehub/lobe-chat
label: Configurations
language: Json
comments_count: 3
repository_stars: 65138
---

Use semantic versioning ranges for dependencies instead of "latest" or overly broad ranges. Avoid "latest" as it can cause caching issues during updates. Maintain minimum required version semantics to ensure compatibility - if your code requires features from version 4.4, specify "^4.4" rather than "^4" to prevent runtime errors when using tools like pnpm with resolution-mode set to lowest. When upgrading dependencies, prefer semantic ranges (e.g., "^0.34.2") over exact version pinning unless there are specific compatibility concerns.

Example:
```json
{
  "dependencies": {
    // ❌ Avoid - caching issues
    "lucide-react": "latest",
    // ❌ Avoid - loses minimum version semantics  
    "zustand": "^4",
    // ✅ Good - preserves minimum required version
    "zustand": "^4.4",
    // ✅ Good - semantic range for upgrades
    "lucide-react": "^0.469.0"
  }
}
```