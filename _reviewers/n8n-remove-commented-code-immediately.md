---
title: Remove commented code immediately
description: Commented-out code should be removed immediately rather than committed
  to the codebase. Keeping commented code creates confusion, adds unnecessary noise,
  and makes the codebase harder to maintain. If code is no longer needed, delete it
  - version control systems will preserve the history if it needs to be referenced
  later.
repository: n8n-io/n8n
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 122978
---

Commented-out code should be removed immediately rather than committed to the codebase. Keeping commented code creates confusion, adds unnecessary noise, and makes the codebase harder to maintain. If code is no longer needed, delete it - version control systems will preserve the history if it needs to be referenced later.

Example of what to avoid:
```typescript
export function useDocumentTitle() {
  // const settingsStore = useSettingsStore();
  // const { releaseChannel } = settingsStore.settings;
  // const suffix = !releaseChannel || releaseChannel === 'stable' 
  //   ? 'n8n' 
  //   : `n8n[${releaseChannel.toUpperCase()}]`;
}
```

Instead, either:
1. Delete the code entirely if it's no longer needed
2. Complete the implementation if the code is still required
3. Create a TODO comment with a clear explanation if the code represents future work

This keeps the codebase clean, current, and easier to understand for all developers.