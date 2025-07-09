---
title: Use concise methods
description: Prefer built-in methods and properties that achieve the same result with
  less code. This improves readability, reduces potential bugs, and makes your code
  more maintainable.
repository: shadcn-ui/ui
label: Code Style
language: Other
comments_count: 2
repository_stars: 90568
---

Prefer built-in methods and properties that achieve the same result with less code. This improves readability, reduces potential bugs, and makes your code more maintainable.

For DOM manipulations, use specialized methods like `classList.toggle()` instead of conditional add/remove operations:

```javascript
// Instead of this:
document.documentElement.classList[isDark ? 'add' : 'remove']('dark');

// Use this more concise approach:
document.documentElement.classList.toggle('dark', isDark);
```

Similarly, avoid redundant styling properties when fewer properties can achieve the desired effect. Review your CSS classes to eliminate unnecessary declarations that don't contribute to the intended visual outcome:

```tsx
// Instead of potentially redundant classes:
<SheetContent className="w-[400px] sm:w-[540px] sm:max-w-none">

// Use only what's necessary:
<SheetContent className="w-[400px] sm:w-[540px]">
```

These simplifications make code easier to read and maintain while reducing the possibility of conflicting declarations.