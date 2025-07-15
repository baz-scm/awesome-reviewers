---
title: Preserve public API stability
description: 'When modifying or extending public interfaces, ensure changes maintain
  backward compatibility and follow proper versioning practices. Key guidelines:

  '
repository: nestjs/nest
label: API
language: TypeScript
comments_count: 5
repository_stars: 71767
---

When modifying or extending public interfaces, ensure changes maintain backward compatibility and follow proper versioning practices. Key guidelines:

1. Make interface additions optional:
```typescript
// Instead of
interface HttpServer {
  newMethod(): void;
}

// Do this
interface HttpServer {
  newMethod?(): void;
}
```

2. Use union types for extending existing types:
```typescript
// Instead of
type Version = string;

// Do this
type Version = string | (string & {}) | ((version: string) => boolean);
```

3. When adding new functionality that could break existing implementations:
- Create a new interface/type that extends the base
- Add configuration options to enable new features
- Wait for major version releases for breaking changes

4. Document version support clearly:
```typescript
@Controller({version: '2.x'})
class MyController {
  @Version('>=2.5.1')
  @Get(':id')
  newMethod() {}

  @Version('<2.5.0')
  @Get(':id')
  legacyMethod() {}
}
```

These practices ensure API consumers can upgrade safely and maintain compatibility with their existing implementations.