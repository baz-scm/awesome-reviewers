---
title: preserve user input focus
description: When implementing reactive state updates that affect input elements,
  always check if the user is currently interacting with the element before applying
  the update. This prevents jarring user experiences where typing gets interrupted
  by state changes.
repository: sveltejs/svelte
label: React
language: JavaScript
comments_count: 3
repository_stars: 83580
---

When implementing reactive state updates that affect input elements, always check if the user is currently interacting with the element before applying the update. This prevents jarring user experiences where typing gets interrupted by state changes.

The most common scenario is when an input's value is bound to reactive state that gets updated from external sources (like API responses or computed values). Without proper checks, these updates can override what the user is currently typing.

```javascript
// Good: Check if input is focused before updating
if (input === document.activeElement) {
  // Skip update to preserve user's current input
  return;
}
input.value = newValue;

// Also applies to React controlled components
function SearchInput({ value, onChange }) {
  const inputRef = useRef();
  
  useEffect(() => {
    // Only update if user isn't currently typing
    if (document.activeElement !== inputRef.current) {
      inputRef.current.value = value;
    }
  }, [value]);
  
  return <input ref={inputRef} onChange={onChange} />;
}
```

This pattern is essential for search inputs, autocomplete fields, and any scenario where external state changes could conflict with user input. It ensures the UI "catches up" to focused inputs rather than disrupting the user's flow.