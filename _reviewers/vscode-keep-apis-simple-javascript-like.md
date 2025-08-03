---
title: Keep APIs simple JavaScript-like
description: Design APIs to be simple and idiomatic to JavaScript/TypeScript while
  maintaining proper encapsulation. Avoid complex type unions, forced undefined parameters,
  or implementation details leaking through interfaces.
repository: microsoft/vscode
label: API
language: TypeScript
comments_count: 6
repository_stars: 174887
---

Design APIs to be simple and idiomatic to JavaScript/TypeScript while maintaining proper encapsulation. Avoid complex type unions, forced undefined parameters, or implementation details leaking through interfaces.

Key principles:
1. Prefer simple classes over discriminated unions
2. Make optional parameters truly optional
3. Maintain clean interface boundaries
4. Follow the API proposal process

Example - Instead of:
```typescript
interface RequestInitiator {
  kind: InitiatorKind.Extension;
  extensionId: string;
} | {
  kind: InitiatorKind.Internal;
  reason: string;
}

function decode(content: Uint8Array, options: { uri: Uri | undefined }): Promise<string>
```

Prefer:
```typescript
class RequestInitiator {
  constructor(
    readonly kind: InitiatorKind,
    readonly identifier: string
  ) {}
}

function decode(content: Uint8Array, options?: { uri?: Uri }): Promise<string>
```