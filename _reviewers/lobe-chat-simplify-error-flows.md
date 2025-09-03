---
title: Simplify error flows
description: Avoid complex, multi-layered error handling that obscures error origins
  and makes debugging difficult. Each error should be handled at the most appropriate
  level without unnecessary re-parsing or nested try-catch blocks.
repository: lobehub/lobe-chat
label: Error Handling
language: TypeScript
comments_count: 3
repository_stars: 65138
---

Avoid complex, multi-layered error handling that obscures error origins and makes debugging difficult. Each error should be handled at the most appropriate level without unnecessary re-parsing or nested try-catch blocks.

Problems with complex error flows:
- Multiple layers of error parsing and transformation make it hard to trace error origins
- Nested try-catch blocks create confusion about which errors are handled where  
- Re-throwing and re-parsing errors adds unnecessary complexity

Instead, handle errors close to their source and use clear, single-responsibility error handling:

```typescript
// ❌ Avoid: Complex nested error handling
async parseFile(fileId: string): Promise<LobeDocument> {
  try {
    const { filePath, file, cleanup } = await this.fileService.downloadFileToLocal(fileId);
    try {
      const fileDocument = await loadFile(filePath);
      // ... processing
    } catch (error) {
      console.error(`File parsing failed:`, error);
      throw error;
    } finally {
      cleanup();
    }
  } catch (error) {
    console.error(`File not found:`, error);
    throw error;
  }
}

// ✅ Better: Single-level error handling with clear responsibility
async parseFile(fileId: string): Promise<LobeDocument> {
  const { filePath, file, cleanup } = await this.fileService.downloadFileToLocal(fileId);
  
  try {
    const fileDocument = await loadFile(filePath);
    // ... processing
    return document;
  } catch (error) {
    console.error(`[${file.name}] File parsing failed:`, error);
    throw error;
  } finally {
    cleanup();
  }
}
```

Keep error handling flows simple and direct to improve code maintainability and debugging experience.