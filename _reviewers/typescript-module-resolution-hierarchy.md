---
title: Module resolution hierarchy
description: When configuring TypeScript projects, establish a clear understanding
  of module and type resolution hierarchies, especially when using different package
  managers like npm or Yarn's Plug'n'Play (PnP).
repository: microsoft/typescript
label: Configurations
language: TypeScript
comments_count: 6
repository_stars: 105378
---

When configuring TypeScript projects, establish a clear understanding of module and type resolution hierarchies, especially when using different package managers like npm or Yarn's Plug'n'Play (PnP).

For module resolution configuration:

1. Use specialized resolution logic for PnP environments rather than fallback approaches to avoid resolution corruptions:
```typescript
// For PnP environments, use direct resolution instead of fallbacks
const searchResult = isPnpAvailable()
    ? tryLoadModuleUsingPnpResolution(Extensions.DtsOnly, typeName, location, moduleState)
    : loadModuleFromNearestNodeModulesDirectory(Extensions.DtsOnly, typeName, location, moduleState);
```

2. Maintain a consistent resolution priority hierarchy: `paths` > `baseUrl` > `typeRoots`. This order respects specificity, with exact matches taking precedence over general directory searches.

3. For path validation with package.json imports/exports that use wildcards, ensure appropriate validation flags are set:
```typescript
vpath.validate(path, vpath.ValidationFlags.Absolute | vpath.ValidationFlags.AllowWildcard);
```

4. When working with workspaces that use PnP, be aware that dependencies with peer dependencies are "virtualized" to unique paths that may require special handling in project references.

These practices help avoid resolution conflicts and ensure consistent behavior across different development environments and package manager configurations.