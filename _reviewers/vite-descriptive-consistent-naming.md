---
title: Descriptive consistent naming
description: 'Choose variable, function, and class names that accurately reflect their
  purpose while maintaining consistency with established patterns in the codebase.
  When the purpose or content of an entity changes, update its name accordingly. This
  applies to:'
repository: vitejs/vite
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 74031
---

Choose variable, function, and class names that accurately reflect their purpose while maintaining consistency with established patterns in the codebase. When the purpose or content of an entity changes, update its name accordingly. This applies to:

1. **Function names**: Use general names for general purposes and specific names for specific purposes.
```javascript
// Before: Overly specific name
function getCodeHash(code: string): string { ... }

// After: More general name that matches its versatile purpose
function getHash(input: string): string { ... }
```

2. **Variable names**: Ensure names accurately reflect the actual content.
```javascript
// Before: Misleading name (contains ids, not urls)
const normalizedAcceptedUrls = new Set<string>()

// After: Name matches content
const resolvedAcceptedDeps = new Set<string>()
```

3. **Collection names**: Use plural forms for collections of items.
```javascript
// Before: Singular form for a collection
public fileToModuleMap = new Map<string, ModuleRunnerNode[]>()

// After: Plural form indicating multiple modules
public fileToModulesMap = new Map<string, ModuleRunnerNode[]>()
```

4. **Parameter names**: Choose names that avoid confusion with similar concepts.
```javascript
// Before: Potentially confusing parameter name
function glob(pattern: string, cwd: string): string[] { ... }

// After: More specific name that avoids confusion
function glob(pattern: string, base: string): string[] { ... }
```

5. **Component names**: Follow established naming patterns within the project.
```javascript
// Before: Inconsistent with project naming patterns
{
  name: 'ember app',
  // ...
}

// After: Follows the project's hyphenated naming pattern
{
  name: 'ember-app',
  // ...
}
```

Always prioritize clarity and accuracy in naming to improve code readability and reduce the likelihood of bugs or misunderstandings.