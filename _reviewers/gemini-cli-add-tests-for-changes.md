---
title: add tests for changes
description: Every code change, whether it's a new feature, bug fix, or refactoring,
  must include corresponding tests. This ensures code quality, prevents regressions,
  and maintains system reliability.
repository: google-gemini/gemini-cli
label: Testing
language: TypeScript
comments_count: 5
repository_stars: 65062
---

Every code change, whether it's a new feature, bug fix, or refactoring, must include corresponding tests. This ensures code quality, prevents regressions, and maintains system reliability.

When adding new functionality:
```typescript
// New feature: paste detection logic
it('should process a paste as a single event', () => {
  renderHook(() => useKeypress(onKeypress, { isActive: true }));
  const pasteText = 'hello world';
  act(() => {
    stdin.paste(pasteText);
    if (isLegacy) {
      vi.advanceTimersByTime(35);
    }
  });
  // Test the new behavior
});
```

When fixing bugs, write tests that would have failed before the fix:
```typescript
// Test for race condition fix
it('should handle concurrent update checks without race conditions', async () => {
  // This test would have failed before the fix
  updateNotifier.mockReturnValue({
    fetchInfo: vi.fn().mockResolvedValue({ current: '1.1.0', latest: '1.0.0' }),
  });
  // Verify the fix works
});
```

Tests serve as documentation of expected behavior and catch regressions during future changes. They should cover the main functionality, edge cases, and error conditions of the code being modified.