---
title: Organize type declarations
description: Structure TypeScript declarations to improve maintainability and developer
  experience. Organize related types into appropriate namespaces and use inheritance
  to avoid duplication.
repository: aws/aws-sdk-js
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 7628
---

Structure TypeScript declarations to improve maintainability and developer experience. Organize related types into appropriate namespaces and use inheritance to avoid duplication.

For service interfaces, place shape definitions in a dedicated sub-namespace to prevent cluttering code completion:

```typescript
// Instead of this:
declare namespace ACM {
  interface AddTagsToCertificateRequest { /*...*/ }
  interface ListCertificatesResponse { /*...*/ }
  // More interfaces...
}

// Do this:
declare namespace ACM {
  // Service properties here
}
declare namespace ACM.Types {
  interface AddTagsToCertificateRequest { /*...*/ }
  interface ListCertificatesResponse { /*...*/ }
  // More interfaces...
}
```

For common properties shared across multiple interfaces or classes, use inheritance or abstract classes instead of duplicating definitions:

```typescript
// Instead of duplicating the same properties in multiple places:
interface ConfigurationOptions {
  // properties and comments
}
class Config {
  // Same properties and comments duplicated
}

// Use inheritance to share definitions:
abstract class BaseConfig {
  // Shared properties with comments
}
class Config extends BaseConfig {
  // Additional properties specific to Config
}
```

This approach improves code completion accuracy, reduces maintenance overhead, and creates a more intuitive API structure.
