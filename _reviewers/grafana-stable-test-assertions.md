---
title: Stable test assertions
description: Write tests that focus on behavior rather than implementation details
  to create more stable and maintainable test suites. Avoid using arbitrary timeouts
  and assertions that frequently break with implementation changes.
repository: grafana/grafana
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 68825
---

Write tests that focus on behavior rather than implementation details to create more stable and maintainable test suites. Avoid using arbitrary timeouts and assertions that frequently break with implementation changes.

**Instead of using arbitrary timeouts:**
```typescript
// Avoid this:
await searchInput.click();
await page.keyboard.type('Datasource tests - MySQL');
await page.waitForTimeout(300); // Brittle: might be too short or too long

// Prefer this:
await searchInput.click();
await page.keyboard.type('Datasource tests - MySQL');
await expect(rowGroup).toHaveCount(1); // Will auto-retry until condition is met
await expect(rows).toHaveCount(expectedLength);
```

**Instead of asserting implementation details:**
```typescript
// Avoid this:
expect(scene.state.$behaviors).toHaveLength(6); // Brittle: breaks when behavior count changes

// Prefer this:
expect(scene.state.$behaviors.find(b => b instanceof CursorSyncBehavior)).toBeDefined(); // Tests actual functionality
```

By focusing tests on behavior and using the testing framework's built-in retry and assertion mechanisms, you'll create more reliable tests that require less maintenance as your codebase evolves.