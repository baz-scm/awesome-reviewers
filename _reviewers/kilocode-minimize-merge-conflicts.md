---
title: minimize merge conflicts
description: When working with upstream codebases, prioritize coding approaches that
  minimize merge conflicts while maintaining functionality. Keep dependency arrays
  in consistent order with upstream code, use CSS classes for conditional styling
  instead of conditional rendering to create smaller diffs, and isolate custom components
  in separate directories. For example,...
repository: kilo-org/kilocode
label: Code Style
language: TSX
comments_count: 4
repository_stars: 7302
---

When working with upstream codebases, prioritize coding approaches that minimize merge conflicts while maintaining functionality. Keep dependency arrays in consistent order with upstream code, use CSS classes for conditional styling instead of conditional rendering to create smaller diffs, and isolate custom components in separate directories. For example, instead of wrapping large code blocks in conditionals, use className approaches:

```tsx
// Prefer this - smaller diff, easier merging
<div className={cn("shrink-0", "w-[70px]", { "hidden": options.length < 2 })}>

// Avoid this - creates large indentation diff
{options.length >= 2 && (
  <div className="shrink-0 w-[70px]">
    // ... large code block
  </div>
)}
```

This approach reduces the likelihood of merge conflicts and makes code reviews easier to follow when syncing with upstream changes.