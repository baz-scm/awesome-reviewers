---
title: Verify configuration paths
description: Ensure configuration property paths are accurate and complete, especially
  for nested configurations and context-specific placement. Many configuration issues
  stem from incorrect or incomplete property paths that prevent features from working
  properly.
repository: nrwl/nx
label: Configurations
language: Markdown
comments_count: 5
repository_stars: 27518
---

Ensure configuration property paths are accurate and complete, especially for nested configurations and context-specific placement. Many configuration issues stem from incorrect or incomplete property paths that prevent features from working properly.

Key areas to verify:

1. **Nested property paths**: Use the full path for nested configurations
   - ✅ `release.docker.repositoryName` 
   - ❌ `release.repositoryName`

2. **Context-specific placement**: Ensure configurations are placed in the correct location based on project setup
   - For inferred targets: place sync generators inside the `nx` property in `package.json`
   - For Docker registries: configure at project level since it needs format like `myorg/app-name`

3. **Scope-appropriate configuration**: Match configuration scope to the intended behavior
   - Project-level configurations for project-specific settings
   - Workspace-level configurations for shared settings

Example of correct nested configuration:
```json
{
  "nx": {
    "release": {
      "docker": {
        "repositoryName": "myorg/my-app"
      }
    }
  }
}
```

Always double-check configuration paths against official documentation and test that configurations work as expected, as incorrect paths often fail silently or produce unexpected behavior.