---
title: Test behavioral differences
description: Tests should verify that different states, modes, or inputs produce meaningfully
  different behaviors, not just that code doesn't crash. Focus on testing state transitions,
  edge cases, and behavioral changes rather than basic existence checks.
repository: google-gemini/gemini-cli
label: Testing
language: TSX
comments_count: 7
repository_stars: 65062
---

Tests should verify that different states, modes, or inputs produce meaningfully different behaviors, not just that code doesn't crash. Focus on testing state transitions, edge cases, and behavioral changes rather than basic existence checks.

Use creative mocking strategies to make visual or complex behaviors testable. For UI components, mock styling functions to produce detectable output differences:

```javascript
// Mock chalk.inverse to make highlighting testable
jest.mock('chalk', () => ({
  inverse: (text) => `[${text}]`
}));

// Test that different states produce different outputs
expect(focusedOutput).toContain('t[e]st'); // highlighted
expect(unfocusedOutput).toContain('test'); // not highlighted
expect(focusedOutput).not.toEqual(unfocusedOutput); // crucial difference check
```

Test comprehensive edge cases and scenarios:
- Different modes (vim mode on/off, focus states)
- Boundary conditions (extremely small widths, empty inputs)
- Complex inputs (multiline text, special characters, escaped spaces)
- State transitions (focus changes, undo/redo operations)

Verify actual behavioral changes rather than just testing that functions were called. For example, test that undo actually restores previous text content, not just that `buffer.undo()` was invoked.