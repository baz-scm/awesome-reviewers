---
title: Constructor over setter
description: Prefer passing configuration through constructor parameters rather than
  setting properties after instantiation. This makes APIs more predictable, enables
  immutability, and clearly communicates required dependencies at creation time. Additionally,
  use consistent method naming conventions like `.invoke()` for primary API methods.
repository: langchain-ai/langchainjs
label: API
language: Other
comments_count: 3
repository_stars: 15004
---

Prefer passing configuration through constructor parameters rather than setting properties after instantiation. This makes APIs more predictable, enables immutability, and clearly communicates required dependencies at creation time. Additionally, use consistent method naming conventions like `.invoke()` for primary API methods.

**Instead of this:**
```javascript
const loader = new GoogleDriveLoader();
loader.recursive = true;
loader.folderId = "YourGoogleDriveFolderId";
```

**Do this:**
```javascript
const loader = new GoogleDriveLoader({
  recursive: true,
  folderId: "YourGoogleDriveFolderId"
});
```

Similarly, when adding methods to an API class, prefer descriptive action names like `invoke()` over generic terms like `call()`. This creates a more intuitive API that follows established patterns across the ecosystem.
