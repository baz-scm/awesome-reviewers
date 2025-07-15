---
title: Descriptive identifier names
description: Choose identifier names (variables, functions, parameters, classes) that
  clearly describe their purpose, content, or behavior. Replace generic terms like
  `value`, `data`, or `options` with more specific alternatives that convey meaning.
repository: nestjs/nest
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 71766
---

Choose identifier names (variables, functions, parameters, classes) that clearly describe their purpose, content, or behavior. Replace generic terms like `value`, `data`, or `options` with more specific alternatives that convey meaning.

For parameters:
```typescript
// Poor: Generic parameter name
async validateFilesOrFile(value: any): Promise<void> {
  // ...
}

// Better: Descriptive parameter name
async validateFilesOrFile(fileOrFiles: any): Promise<void> {
  // ...
}
```

For method names:
```typescript
// Poor: Ambiguous method name
protected mergeOptions(opts1, opts2) { ... }

// Better: Purpose-specific method name
protected mergePacketOptions(opts1, opts2) { ... }
```

For properties:
```typescript
// Poor: Vague property name
private readonly signalsListening: string[] = new Array<string>();

// Better: Purpose-specific property name
private readonly activeShutdownSignals: string[] = new Array<string>();
```

For boolean variables, use names that clearly indicate the condition they represent:
```typescript
// Poor: Cryptic boolean name
const cacheManagerIsv5OrGreater = 'memoryStore' in cacheManager;

// Better: Clear condition description
const isCacheManagerV5OrLater = 'memoryStore' in cacheManager;
```

Methods with prefixes like "is", "has", or "should" must return boolean values:
```typescript
// Misleading: Method name suggests boolean return
public shouldFlushLogsOnOverride() {
  // Method updates state but doesn't return boolean
}

// Better: Property for state, method returns boolean
public shouldFlushLogsOnOverride: boolean;
public flushLogsOnOverride(): void { /* ... */ }
```

Clear, descriptive naming reduces cognitive load, improves code readability, and helps prevent bugs from misinterpreting an identifier's purpose.