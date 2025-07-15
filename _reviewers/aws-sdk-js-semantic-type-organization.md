---
title: Semantic type organization
description: Organize types and interfaces in intuitive namespace hierarchies and
  use specific types instead of generic ones. Types should be accessible through logically
  related namespaces, and method signatures should accurately reflect their parameters
  and return values. This improves code clarity, discoverability, and type safety.
repository: aws/aws-sdk-js
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 7628
---

Organize types and interfaces in intuitive namespace hierarchies and use specific types instead of generic ones. Types should be accessible through logically related namespaces, and method signatures should accurately reflect their parameters and return values. This improves code clarity, discoverability, and type safety.

```typescript
// Prefer this (specific types, logical organization)
const converter: Converter = DynamoDB.Converter;
function resolvePromise(): Promise<Credentials> { /* ... */ }

// Instead of these (generic types, unintuitive organization)
const converter: any = DynamoDB.Converter;
const options: DynamoDB.DocumentClient.ConverterOptions = { /* ... */ }; // accessing through DocumentClient when logically belongs to Converter
function resolvePromise(): Promise<any> { /* ... */ }
```
