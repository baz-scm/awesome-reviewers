---
title: Extract duplicate code
description: When you notice code patterns being repeated across multiple locations,
  extract them into reusable functions or constants to improve maintainability and
  follow DRY principles.
repository: prisma/prisma
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 42967
---

When you notice code patterns being repeated across multiple locations, extract them into reusable functions or constants to improve maintainability and follow DRY principles.

Look for these common duplication patterns:
- **Identical logic blocks**: Extract into shared functions
- **Repeated literal arrays/objects**: Extract into named constants  
- **Similar data transformations**: Create utility functions
- **Complex type conversions**: Move to dedicated helper functions

Example from the codebase:
```typescript
// Before: Duplicated logic in multiple methods
async storeCredentials(data: AuthFile): Promise<void> {
  const authData: AuthFile = { tokens: this.loadedCredentials }
  await mkdir(path.dirname(this.authFilePath), { recursive: true })
  await writeFile(this.authFilePath, JSON.stringify(authData, null, 2))
}

async deleteCredentials(workspaceId: string): Promise<void> {
  this.loadedCredentials = this.loadedCredentials?.filter((c) => c.workspaceId !== workspaceId) || []
  const data: AuthFile = { tokens: this.loadedCredentials }
  await mkdir(path.dirname(this.authFilePath), { recursive: true })
  await writeFile(this.authFilePath, JSON.stringify(data, null, 2))
}

// After: Extract shared logic
private async writeAuthFile(data: AuthFile): Promise<void> {
  await mkdir(path.dirname(this.authFilePath), { recursive: true })
  await writeFile(this.authFilePath, JSON.stringify(data, null, 2))
}
```

This practice reduces maintenance burden, eliminates inconsistencies, and makes code changes easier to implement across the codebase.