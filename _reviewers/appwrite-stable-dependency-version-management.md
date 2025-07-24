---
title: Stable dependency version management
description: Always use stable, well-defined version constraints in configuration
  files to ensure reproducible builds and prevent unexpected behavior. Avoid using
  development branches for production dependencies.
repository: appwrite/appwrite
label: Configurations
language: Json
comments_count: 7
repository_stars: 51959
---

Always use stable, well-defined version constraints in configuration files to ensure reproducible builds and prevent unexpected behavior. Avoid using development branches for production dependencies.

Key practices:
1. Use semantic versioning constraints:
   - Use `^` for minor updates: `"package": "^1.2.3"`
   - Use `~` for patch updates: `"package": "~1.2.3"`
   - Pin exact versions when needed: `"package": "1.2.3"`

2. Never use dev branches in production unless absolutely necessary. If required:
   ```json
   {
     "require": {
       "package": "1.2.*",
     },
     "minimum-stability": "dev",
     "prefer-stable": true
   }
   ```

3. Always commit lock files (e.g., composer.lock) to ensure consistent dependency versions across environments.

4. When updating versions, update all related configuration files and documentation to maintain consistency.