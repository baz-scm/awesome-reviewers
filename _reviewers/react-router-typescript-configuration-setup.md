---
title: TypeScript configuration setup
description: Ensure proper TypeScript configuration for generated types and development
  workflow. This includes setting up gitignore patterns, configuring tsconfig.json
  for type generation, and integrating typegen into build scripts.
repository: remix-run/react-router
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 55270
---

Ensure proper TypeScript configuration for generated types and development workflow. This includes setting up gitignore patterns, configuring tsconfig.json for type generation, and integrating typegen into build scripts.

When working with frameworks that generate types (like React Router v7), follow these configuration steps:

1. **Add generated directories to gitignore**:
```txt
.react-router/
```

2. **Configure tsconfig.json for generated types**:
```json
{
  "include": [".react-router/types/**/*"],
  "compilerOptions": {
    "rootDirs": [".", "./.react-router/types"]
  }
}
```

3. **Integrate typegen into build scripts**:
```json
{
  "scripts": {
    "typecheck": "react-router typegen && tsc"
  }
}
```

This configuration ensures that generated types are properly excluded from version control, TypeScript can locate and use the generated types correctly, and the development workflow includes type generation as part of the build process. The `rootDirs` configuration allows importing generated types as if they were sibling files, improving developer experience.