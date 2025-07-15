---
title: Document CI/CD changes
description: 'Always document changes to CI/CD configurations and scripts, and ensure
  pull requests remain focused on their intended purpose. When modifying build scripts,
  dependencies, or deployment processes:'
repository: nestjs/nest
label: CI/CD
language: Json
comments_count: 2
repository_stars: 71766
---

Always document changes to CI/CD configurations and scripts, and ensure pull requests remain focused on their intended purpose. When modifying build scripts, dependencies, or deployment processes:

1. Review all dependency changes to ensure they are necessary for the current work
2. Keep changes focused and avoid unintended modifications that may affect the build pipeline
3. If simplifying or removing build/deployment scripts, document the new procedure clearly

**Example:**
```diff
# When removing scripts from package.json
@@ -2,24 +2,13 @@
   "name": "nestjs",
   "version": "5.0.0",
   "description": "Modern, fast, powerful node.js web framework",
+  "private": true,
   "scripts": {
-    "publish": "./node_modules/.bin/lerna publish --exact -m \"chore(@nestjs) publish %s release\"",
+    // Scripts removed
   
   // Add a comment explaining the change
   // Example: "// Publish process simplified - run 'yarn run lerna publish' directly"
```

Adding a CONTRIBUTING.md or updating README.md with new procedures when removing or changing build scripts ensures that the team can maintain continuity in the CI/CD workflow.