---
title: avoid non-null assertions
description: Avoid using the non-null assertion operator (`!`) and instead use union
  types or explicit null checks for better type safety. Non-null assertions bypass
  TypeScript's null safety checks and can lead to runtime errors if the assumption
  is incorrect.
repository: google-gemini/gemini-cli
label: Null Handling
language: TypeScript
comments_count: 2
repository_stars: 65062
---

Avoid using the non-null assertion operator (`!`) and instead use union types or explicit null checks for better type safety. Non-null assertions bypass TypeScript's null safety checks and can lead to runtime errors if the assumption is incorrect.

**Preferred approach - Use union types:**
```typescript
// Instead of using non-null assertion
return {
  filePath,
  relativePathForDisplay, 
  fileReadResult: fileReadResult!.llmContent  // ❌ Unsafe
};

// Use union types to make success cases explicit
type FileResult = 
  | { success: true; fileReadResult: FileReadResult }
  | { success: false; reason: string };

// TypeScript now properly narrows the type
if (fileResult.success) {
  // fileReadResult is guaranteed to exist here
  return fileResult.fileReadResult.llmContent; // ✅ Safe
}
```

**When explicit checks are safer:**
```typescript
// Instead of non-null assertion
return this.contentGenerator!; // ❌ Bypasses safety

// Use explicit null check with clear error handling
if (!this.contentGenerator) {
  throw new Error('Content generator not initialized');
}
return this.contentGenerator; // ✅ Safe and clear
```

This approach makes null handling explicit in the type system and prevents runtime errors from incorrect assumptions about null values.