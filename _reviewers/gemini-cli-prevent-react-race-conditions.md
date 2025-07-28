---
title: Prevent React race conditions
description: When building React components that handle rapid user input or manage
  complex interdependent state, consolidate state management to prevent race conditions
  that occur when multiple events are processed in the same React event loop.
repository: google-gemini/gemini-cli
label: React
language: TypeScript
comments_count: 3
repository_stars: 65062
---

When building React components that handle rapid user input or manage complex interdependent state, consolidate state management to prevent race conditions that occur when multiple events are processed in the same React event loop.

**Key strategies:**

1. **Use useReducer for complex interdependent state** instead of multiple useState calls. This centralizes state logic, improves performance by reducing re-renders, and eliminates potential race conditions from multiple state updates.

2. **Integrate utility functions with centralized state** rather than operating on potentially stale closures or separate state variables.

**Example:**
```typescript
// ❌ Problematic: Multiple useState calls for interdependent state
const [mode, setMode] = useState('NORMAL');
const [count, setCount] = useState(0);
const [pendingG, setPendingG] = useState(false);
const [pendingD, setPendingD] = useState(false);

// ❌ Utility functions operating separately
const findNextWordStart = (text: string, offset: number) => {
  // May operate on stale state when multiple keystrokes occur rapidly
};

// ✅ Better: Single useReducer for interdependent state
const [state, dispatch] = useReducer(vimReducer, {
  mode: 'NORMAL',
  count: 0,
  pendingG: false,
  pendingD: false,
});

// ✅ Integrate utilities with centralized state management
// Move utility functions into the same state management system
// to ensure they operate on current state
```

This approach prevents issues where "multiple keystrokes need to be processed in the same React event loop" and eliminates race conditions from managing complex state machines in React components.