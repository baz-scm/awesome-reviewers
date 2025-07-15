---
title: Preserve API interface stability
description: 'When modifying or extending public API interfaces, ensure backward compatibility
  and proper versioning. Follow these guidelines:


  1. Make interface additions optional to avoid breaking changes:'
repository: nestjs/nest
label: API
language: TypeScript
comments_count: 5
repository_stars: 71766
---

When modifying or extending public API interfaces, ensure backward compatibility and proper versioning. Follow these guidelines:

1. Make interface additions optional to avoid breaking changes:
```typescript
// Instead of adding required methods
interface HttpServer {
  get(): void;
  newMethod(): void; // Breaking change!
}

// Make additions optional
interface HttpServer {
  get(): void;
  newMethod?(): void; // Non-breaking change
}
```

2. Support versioning through explicit version types:
```typescript
// Allow flexible version handling
export interface CustomVersioningOptions {
  type: VersioningType.CUSTOM;
  extractor: (request: any) => string | string[];
}

@Controller({
  version: '1',
  versioningOptions: customOptions
})
```

3. When evolving interfaces:
- Add new methods as optional properties
- Use union types for backward compatibility
- Document breaking changes for major version releases
- Consider providing migration paths for deprecated features

This approach maintains API stability while enabling controlled evolution of the interface contract.