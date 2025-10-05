---
title: Environment file management
description: 'Ensure proper handling of environment files by following these practices:
  (1) Add actual environment files (`.env`, `.env.local`, etc.) to `.gitignore` to
  prevent sensitive data from being committed, (2) Include example environment files
  (`.env.example`) in version control to help other developers understand required
  configuration, and (3) Add clear...'
repository: TanStack/router
label: Configurations
language: Other
comments_count: 3
repository_stars: 11590
---

Ensure proper handling of environment files by following these practices: (1) Add actual environment files (`.env`, `.env.local`, etc.) to `.gitignore` to prevent sensitive data from being committed, (2) Include example environment files (`.env.example`) in version control to help other developers understand required configuration, and (3) Add clear documentation in example files explaining how to use them.

Example `.gitignore` entry:
```
# Environment files
.env
.env.local
.env.*.local
```

Example `.env.example` with documentation:
```
# Copy this file as `.env.local` and fill in these values from your service console
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
```

This approach ensures projects remain cloneable while protecting sensitive configuration data and providing clear setup instructions for new developers.