---
title: Ensure proper async context
description: Always wrap asynchronous operations (await, suspend functions, try-await)
  in the appropriate language-specific async context. Top-level await is generally
  not supported and will cause runtime errors.
repository: appwrite/appwrite
label: Concurrency
language: Markdown
comments_count: 4
repository_stars: 51959
---

Always wrap asynchronous operations (await, suspend functions, try-await) in the appropriate language-specific async context. Top-level await is generally not supported and will cause runtime errors.

**JavaScript/Node.js (CommonJS):**
```javascript
// ❌ Incorrect - top-level await
const result = await databases.createDocuments(...);

// ✅ Correct - async IIFE with error handling
(async () => {
  try {
    const result = await databases.createDocuments(...);
    console.log(result);
  } catch (error) {
    console.error(error);
  }
})();
```

**Swift:**
```swift
// ❌ Incorrect - try-await outside async context
let documentList = try await databases.upsertDocuments(...);

// ✅ Correct - Task with do-catch
Task {
  do {
    let documentList = try await databases.upsertDocuments(...);
    print(documentList);
  } catch {
    print("Error:", error);
  }
}
```

**C#:**
```csharp
// ❌ Incorrect - await outside async method
DocumentList result = await databases.CreateDocuments(...);

// ✅ Correct - async method
public static async Task Main(string[] args)
{
    DocumentList result = await databases.CreateDocuments(...);
    Console.WriteLine(result);
}
```

Always include appropriate error handling for asynchronous operations to prevent unhandled promise/task rejections and improve debugging.