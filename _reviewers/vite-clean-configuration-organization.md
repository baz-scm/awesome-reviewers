---
title: Clean configuration organization
description: Organize configuration settings logically and avoid redundancy in project
  configuration files. Group related options into appropriate sections, eliminate
  duplicated settings (especially those already provided by extended configurations),
  and document non-obvious choices with explanatory comments.
repository: vitejs/vite
label: Configurations
language: Json
comments_count: 4
repository_stars: 74031
---

Organize configuration settings logically and avoid redundancy in project configuration files. Group related options into appropriate sections, eliminate duplicated settings (especially those already provided by extended configurations), and document non-obvious choices with explanatory comments.

TypeScript configurations should:
- Place options in semantically appropriate sections (e.g., linting options in "Linting" section)
- Avoid repeating options already provided by extended configurations
- Remove options that are already implied by other settings

```diff
// In tsconfig.json
{
  "extends": "@tsconfig/ember",
  "compilerOptions": {
    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
-   "isolatedModules": true,
+   "verbatimModuleSyntax": true, // In "Linting" section below
    
    /* Linting */
    "strict": true,
+   "verbatimModuleSyntax": true, // Moved from "Bundler mode"
-   "strictBuiltinIteratorReturn": true, // Redundant with "strict: true"
  }
}
```

For new plugins or packages, prefer modern module configurations:
```json
{
  "name": "@vitejs/plugin-example",
  "type": "module",  // Prefer ESM for new packages
  "files": ["dist"]
}
```

This approach improves maintainability and helps onboard new developers by making configuration intent clearer while reducing conflicting settings.