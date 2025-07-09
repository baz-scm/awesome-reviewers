---
title: Complete hook dependency arrays
description: Ensure all hooks (useEffect, useCallback, useMemo) explicitly list every
  dependency used within their callback functions. Missing dependencies can lead to
  stale closures, unexpected behaviors, and hard-to-debug issues.
repository: elie222/inbox-zero
label: React
language: TSX
comments_count: 4
repository_stars: 8267
---

Ensure all hooks (useEffect, useCallback, useMemo) explicitly list every dependency used within their callback functions. Missing dependencies can lead to stale closures, unexpected behaviors, and hard-to-debug issues.

Example of proper dependency management:

```typescript
// ❌ Incomplete dependencies
useEffect(() => {
  if (textareaRef.current) {
    const finalValue = domValue || localStorageInput || "";
    setInput(finalValue);
    adjustHeight();
  }
}, []); // Missing localStorageInput and setInput

// ✅ Complete dependencies
useEffect(() => {
  if (textareaRef.current) {
    const finalValue = domValue || localStorageInput || "";
    setInput(finalValue);
    adjustHeight();
  }
}, [localStorageInput, setInput]);

// Same applies for useCallback
const handleAction = useCallback(
  async (index: number, action: string) => {
    const item = items[index];
    if (!item) return;
    onAction(item);
    refreshData();
  },
  [items, onAction, refreshData] // List all used dependencies
);
```

Key points:
- List every variable, function, and prop used inside the callback
- Don't silence linter warnings without proper justification
- Consider refactoring if dependency arrays become too large
- Use dependency arrays to optimize re-renders and prevent infinite loops