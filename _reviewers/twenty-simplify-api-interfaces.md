---
title: simplify API interfaces
description: Keep API interfaces simple and focused by avoiding unnecessary input
  wrapping, extracting context parameters appropriately, and limiting exposure of
  internal implementation details.
repository: twentyhq/twenty
label: API
language: TypeScript
comments_count: 6
repository_stars: 35477
---

Keep API interfaces simple and focused by avoiding unnecessary input wrapping, extracting context parameters appropriately, and limiting exposure of internal implementation details.

**Key principles:**
- **Flatten input structures**: Avoid wrapping single properties in input objects. Put properties directly at the root level instead of nesting them unnecessarily.
- **Extract context parameters**: Remove workspace/tenant identifiers from input objects and pass them as separate parameters to maintain clear separation of concerns.
- **Use appropriate types**: Choose specific input/output types over generic database entities. Prefer `CreateViewFieldInput` over `Partial<Entity>` and `UpdateInput` over `QueryDeepPartialEntity`.
- **Limit API exposure**: Don't expose internal fields like `workspaceId` in public APIs when users don't need that information.
- **Provide specific operations**: Instead of generic flexible APIs, offer specific operations like `switchToYearly()` or `cancel()` rather than exposing the entire data model.

**Example:**
```typescript
// ❌ Avoid unnecessary input wrapping
async createPublicDomain(
  @Args('input') { domain }: PublicDomainInput,
) { ... }

// ✅ Put properties directly at root level
async createPublicDomain(
  @Args('domain') domain: string,
) { ... }

// ❌ Don't mix context with business data
async create(
  viewFieldData: Partial<ViewFieldEntity>, // contains workspaceId
) { ... }

// ✅ Extract context parameters
async create(
  viewFieldData: CreateViewFieldInput,
  workspaceId: string,
) { ... }
```

This approach reduces API complexity, improves type safety, and maintains clear boundaries between public interfaces and internal implementation details.