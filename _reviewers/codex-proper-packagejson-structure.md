---
title: Proper package.json structure
description: 'Maintain clean and properly structured package.json files by following
  these principles:


  1. Categorize dependencies correctly - place development tools and testing libraries
  in `devDependencies`, not in regular `dependencies`. This ensures smaller production
  builds and clearer dependency management.'
repository: openai/codex
label: Configurations
language: Json
comments_count: 2
repository_stars: 31275
---

Maintain clean and properly structured package.json files by following these principles:

1. Categorize dependencies correctly - place development tools and testing libraries in `devDependencies`, not in regular `dependencies`. This ensures smaller production builds and clearer dependency management.

2. Avoid creating custom npm scripts that merely duplicate functionality already available through standard CLI commands.

Example of proper dependency categorization:
```diff
 {
   "dependencies": {
     "react": "^18.2.0",
     "openai": "^4.89.0",
-    "js-yaml": "^4.1.0",
   },
   "devDependencies": {
+    "js-yaml": "^4.1.0",
     "typescript": "^5.0.0",
     "jest": "^29.0.0"
   },
   "scripts": {
     "build": "tsc",
-    "husky:add": "husky add"
   }
 }
```

This approach keeps configuration files clean, minimizes production build size, and leverages standard tools as intended.