---
title: Validate before expensive operations
description: Perform lightweight validation checks before executing expensive operations
  to avoid unnecessary resource consumption. This is especially important in hot paths
  or frequently called functions.
repository: microsoft/vscode
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 174887
---

Perform lightweight validation checks before executing expensive operations to avoid unnecessary resource consumption. This is especially important in hot paths or frequently called functions.

Key practices:
1. Use file system operations instead of process spawning
2. Check file sizes before reading entire files
3. Filter collections before heavy processing
4. Use specific API methods instead of broad queries

Example - Before:
```typescript
async function getWorktrees(): Promise<Worktree[]> {
    // Spawns process on hot path
    const result = await spawn('git', ['worktree', 'list']);
    return parseWorktrees(result);
}
```

After:
```typescript
async function getWorktrees(): Promise<Worktree[]> {
    // Use fs operations first
    const hasWorktrees = await fs.exists('.git/worktrees');
    if (!hasWorktrees) {
        return [];
    }
    // Only spawn process if needed
    const result = await spawn('git', ['worktree', 'list']);
    return parseWorktrees(result);
}
```