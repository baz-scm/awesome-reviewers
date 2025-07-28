---
title: Match function names to behavior
description: Function names and their documentation must accurately reflect what the
  function actually does. When a function handles more data than its name suggests,
  either rename the function or split the functionality.
repository: llvm/llvm-project
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 33702
---

Function names and their documentation must accurately reflect what the function actually does. When a function handles more data than its name suggests, either rename the function or split the functionality.

In the example below, `formatDate()` actually formats both date and time components, making the name misleading:

```typescript
/**
 * Formats the given date as a string in the form "YYYYMMdd".
 */
function formatDate(date: Date): string {
    const year = date.getFullYear().toString().padStart(4, "0");
    const month = (date.getMonth() + 1).toString().padStart(2, "0");
    const day = date.getDate().toString().padStart(2, "0");
    const hour = date.getHours().toString().padStart(2, "0");
    const minute = date.getMinutes().toString().padStart(2, "0");
    const seconds = date.getSeconds().toString().padStart(2, "0");
    return year + month + day + hour + minute + seconds;
}
```

Better approaches:
- Rename to `formatDateTime()` and update documentation to "YYYYMMddTHHMMSS"
- Keep `formatDate()` but remove time components
- Split into separate `formatDate()` and `formatTime()` functions

This prevents confusion about what data the function processes and ensures the API is self-documenting.