---
title: organize code by responsibility
description: Place code at the appropriate abstraction level and extract complex logic
  to dedicated modules. Large files like App.tsx and gemini.tsx should focus on their
  core responsibilities, with specific functionality moved to specialized components
  or utility files.
repository: google-gemini/gemini-cli
label: Code Style
language: TSX
comments_count: 9
repository_stars: 65062
---

Place code at the appropriate abstraction level and extract complex logic to dedicated modules. Large files like App.tsx and gemini.tsx should focus on their core responsibilities, with specific functionality moved to specialized components or utility files.

**When to extract:**
- Functions that handle specific domains (e.g., auto-updates, keystroke handling)
- Logic that doesn't require the full context of the current component
- Complex algorithms that can be tested independently

**When to move to lower abstraction:**
- Logic that operates on data structures directly (e.g., TextBuffer operations)
- Functionality that bypasses existing utilities (use colors.ts instead of direct theme manager calls)

**Example:**
```typescript
// Instead of handling keystrokes directly in App.tsx:
if (key.ctrl && input === 'o') {
  setShowErrorDetails((prev) => !prev);
} else if (key.ctrl && input === 't') {
  // complex logic...
}

// Extract to keystrokeHandler.ts:
const keystrokeHandlers = [
  {
    input: 'o',
    ctrl: true,
    handler: () => setShowErrorDetails((prev) => !prev),
  },
  // ...
];
```

This approach keeps files focused, improves testability, and makes the codebase more maintainable by ensuring each module has a clear, single responsibility.