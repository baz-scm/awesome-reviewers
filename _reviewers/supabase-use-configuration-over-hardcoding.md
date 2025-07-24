---
title: Use configuration over hardcoding
description: Always use configuration constants instead of hardcoding values directly
  in the code. This improves maintainability and reduces errors when values need to
  change across different environments or contexts.
repository: supabase/supabase
label: Configurations
language: TSX
comments_count: 3
repository_stars: 86070
---

Always use configuration constants instead of hardcoding values directly in the code. This improves maintainability and reduces errors when values need to change across different environments or contexts.

Key practices:
1. Define configuration values in a centralized location
2. Reference these values using constants or environment variables
3. Make text and numerical values dynamic when they represent configurable limits or settings

Example:
```typescript
// ❌ Bad
const StorageSettings = () => {
  return (
    <div>
      Maximum size in bytes of a file that can be uploaded is 500 GB
    </div>
  );
}

// ✅ Good
const StorageSettings = () => {
  return (
    <div>
      Maximum size in bytes of a file that can be uploaded is {
        formatBytes(STORAGE_FILE_SIZE_LIMIT_MAX_BYTES_UNCAPPED)
      }
    </div>
  );
}
```