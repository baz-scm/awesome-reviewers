---
title: Complete OpenAPI annotations
description: Ensure all API endpoints have complete and accurate OpenAPI annotations
  to support proper SDK generation and documentation. Use appropriate decorators,
  include all necessary metadata, and verify that generated SDKs work correctly.
repository: novuhq/novu
label: API
language: TypeScript
comments_count: 8
repository_stars: 37700
---

Ensure all API endpoints have complete and accurate OpenAPI annotations to support proper SDK generation and documentation. Use appropriate decorators, include all necessary metadata, and verify that generated SDKs work correctly.

Key requirements:
- Use `@ApiPropertyOptional` for optional fields instead of `@ApiProperty` with `required: false`
- Add `additionalProperties: true` for object types to enable proper SDK type generation
- Include `nullable: true` when fields can be null (different from optional)
- Use `@ApiHideProperty` conditionally when properties should not appear in public documentation
- Ensure response decorators properly override schemas rather than deleting them
- Add complete metadata including examples, descriptions, and type information

Example of proper annotations:
```typescript
@ApiPropertyOptional({
  description: 'The data sent with the notification.',
  type: 'object',
  nullable: true,
  example: { key: 'value' },
  additionalProperties: true
})
data?: Record<string, unknown>;

// Conditional hiding for internal-only properties
@ApiHideProperty() // when IS_DOCKER_HOSTED !== 'true'
@IsOptional()
@IsNumber()
priority?: number;
```

This ensures accurate documentation generation, proper SDK type inference, and consistent API behavior across all client libraries.