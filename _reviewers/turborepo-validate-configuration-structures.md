---
title: Validate configuration structures
description: 'Ensure configuration files and schemas adhere to their expected structure,
  location, and uniqueness constraints. When supporting multiple configuration file
  formats (e.g., both .json and .jsonc extensions), implement validation to prevent
  conflicting configurations:'
repository: vercel/turborepo
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 28115
---

Ensure configuration files and schemas adhere to their expected structure, location, and uniqueness constraints. When supporting multiple configuration file formats (e.g., both .json and .jsonc extensions), implement validation to prevent conflicting configurations:

```typescript
// Good practice: Check for conflicting config files
function resolveTurboConfigPath(workspacePath: string) {
  const turboJsonPath = path.join(workspacePath, "turbo.json");
  const turboJsoncPath = path.join(workspacePath, "turbo.jsonc");
  
  const turboJsonExists = fs.existsSync(turboJsonPath);
  const turboJsoncExists = fs.existsSync(turboJsoncPath);
  
  if (turboJsonExists && turboJsoncExists) {
    throw new Error(`Found both turbo.json and turbo.jsonc in ${workspacePath}. Please use only one.`);
  }
  
  // Return appropriate config path...
}
```

When defining configuration schemas, ensure properties are placed at their correct hierarchical level and not incorrectly nested. Regularly verify that configuration documentation matches the actual implementation, especially after making changes that affect how users configure your tools.

When users report confusion about configuration usage, prioritize updating documentation and examples to reflect the current expected configuration format.