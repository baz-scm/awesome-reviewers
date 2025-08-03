---
title: Handle errors with specificity
description: 'Always handle errors specifically and explicitly, avoiding generic catch
  blocks that mask or ignore errors. Ensure proper resource cleanup and consistent
  error propagation. Key practices:'
repository: microsoft/vscode
label: Error Handling
language: TypeScript
comments_count: 6
repository_stars: 174887
---

Always handle errors specifically and explicitly, avoiding generic catch blocks that mask or ignore errors. Ensure proper resource cleanup and consistent error propagation. Key practices:

1. Match specific error conditions instead of using catch-all blocks
2. Clean up resources even in error paths
3. Propagate errors appropriately rather than swallowing them
4. Handle errors consistently across similar scenarios

Example of proper error handling:

```typescript
private async getWorktreesFS(): Promise<Worktree[]> {
    const worktreesPath = path.join(this.repositoryRoot, '.git', 'worktrees');
    try {
        const raw = await fs.readdir(worktreesPath);
        // ... processing ...
    } catch (err) {
        // Handle specific error condition
        if (/ENOENT/.test(err.message)) {
            return [];
        }
        // Propagate unexpected errors
        throw err;
    } finally {
        // Clean up resources
        this.disposables.dispose();
    }
}
```

Bad practice to avoid:
```typescript
try {
    // ... operations ...
} catch (err) {
    // DON'T: Silently swallow errors
}
```