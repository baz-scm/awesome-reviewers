---
title: Consistent code examples
description: Maintain consistent formatting and styling in code examples throughout
  your NestJS application documentation. This ensures developers can quickly understand
  dependency injection patterns, module structures, and decorator usage.
repository: fastapi/fastapi
label: NestJS
language: Markdown
comments_count: 5
repository_stars: 86871
---

Maintain consistent formatting and styling in code examples throughout your NestJS application documentation. This ensures developers can quickly understand dependency injection patterns, module structures, and decorator usage.

When documenting your NestJS code:

1. Use consistent syntax highlighting for TypeScript code blocks
2. Include complete examples that show the context of dependency injection
3. For terminal output examples, use standardized styling with clear visual indicators
4. When showing installation instructions, always include comprehensive dependency commands

**Example for documentation:**

```typescript
// Clear module structure with dependency injection
@Module({
  imports: [ConfigModule.forRoot()],
  controllers: [UsersController],
  providers: [
    {
      provide: 'DATABASE_CONNECTION',
      useFactory: async (configService: ConfigService) => {
        // Implementation that demonstrates the dependency clearly
        return createConnection({
          type: configService.get('DB_TYPE'),
          host: configService.get('DB_HOST')
        });
      },
      inject: [ConfigService]
    },
    UsersService
  ],
  exports: [UsersService]
})
export class UsersModule {}
```

For installation instructions:

```console
$ npm install @nestjs/core @nestjs/common rxjs reflect-metadata
```

Consistent documentation makes onboarding easier and reduces confusion about proper implementation patterns.