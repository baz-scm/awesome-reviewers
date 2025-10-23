---
title: Use parameter objects
description: Design API methods to accept parameter objects instead of individual
  parameters or complex optional fields. This approach makes interfaces more maintainable
  and flexible when requirements evolve, avoiding breaking changes when adding or
  removing fields.
repository: dyad-sh/dyad
label: API
language: TypeScript
comments_count: 2
repository_stars: 16903
---

Design API methods to accept parameter objects instead of individual parameters or complex optional fields. This approach makes interfaces more maintainable and flexible when requirements evolve, avoiding breaking changes when adding or removing fields.

Instead of destructuring parameters or using many optional fields:
```typescript
// Avoid - breaks when parameters change
public async editCustomLanguageModelProvider({
  id,
  name,
  apiKey,
  baseUrl
}: {
  id: string;
  name?: string;
  apiKey?: string;
  baseUrl?: string;
}) {
  return this.invoke("edit-provider", { id, name, apiKey, baseUrl });
}

// Avoid - complex optional schemas
export const ProviderSettingSchema = z.object({
  apiKey: SecretSchema.optional(),
  vertexProjectId: z.string().optional(),
  azureEndpoint: z.string().optional(),
  // ... many optional fields
});
```

Prefer parameter objects and proper type modeling:
```typescript
// Better - stable interface that accepts parameter objects
editCustomLanguageModelProvider(params: EditCustomLanguageModelProviderParams) {
  return this.invoke("edit-provider", params);
}

// Better - use unions for distinct parameter sets
export const ProviderSettingSchema = z.union([
  RegularProviderSettingSchema,
  VertexProviderSettingSchema,
  AzureProviderSettingSchema
]);
```

This pattern keeps method signatures stable while allowing the parameter types to evolve independently.