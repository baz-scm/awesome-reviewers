---
title: Use absolute paths
description: When specifying file paths in configuration files (like ESLint or TypeScript
  configs), use absolute paths rather than relative paths to avoid path resolution
  issues. Tools may interpret relative paths differently based on their internal working
  directory, leading to unexpected behavior.
repository: microsoft/typescript
label: Configurations
language: Other
comments_count: 2
repository_stars: 105378
---

When specifying file paths in configuration files (like ESLint or TypeScript configs), use absolute paths rather than relative paths to avoid path resolution issues. Tools may interpret relative paths differently based on their internal working directory, leading to unexpected behavior.

Example:
```javascript
// Problematic - using relative paths
parserOptions: {
  projectService: true,
  defaultProject: "./scripts/tsconfig.json",
}

// Better - using absolute paths
parserOptions: {
  tsconfigRootDir: __dirname,
  projectService: {
    defaultProject: path.join(__dirname, "scripts", "tsconfig.json"),
  }
}
```

This practice prevents issues like the one observed where a tool internally calls `getParsedCommandLineOfConfigFile` with a relative path, but then sets the current working directory incorrectly, causing the wrong file to be loaded.