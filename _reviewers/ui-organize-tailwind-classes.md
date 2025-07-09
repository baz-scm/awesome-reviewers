---
title: Organize tailwind classes
description: Structure your Tailwind CSS classes for readability and maintainability.
  Instead of long chains of conditional classes with `&&` operators, use object syntax
  with clear naming patterns. This improves code readability and makes maintenance
  significantly easier.
repository: shadcn-ui/ui
label: Code Style
language: TSX
comments_count: 7
repository_stars: 90568
---

Structure your Tailwind CSS classes for readability and maintainability. Instead of long chains of conditional classes with `&&` operators, use object syntax with clear naming patterns. This improves code readability and makes maintenance significantly easier.

**Instead of this:**
```jsx
className={cn(
  "h-9 w-9 p-0 font-normal",
  modifiers?.today && "bg-accent text-accent-foreground",
  modifiers?.selected && "bg-primary text-primary-foreground hover:bg-primary hover:text-primary-foreground",
  modifiers?.outside && "text-muted-foreground opacity-50 pointer-events-none",
  // many more conditions
)}
```

**Do this instead:**
```jsx
className={cn({
  "h-9 w-9 p-0 font-normal": true,
  "bg-accent text-accent-foreground": modifiers?.today,
  "bg-primary text-primary-foreground hover:bg-primary hover:text-primary-foreground": modifiers?.selected,
  "text-muted-foreground opacity-50 pointer-events-none": modifiers?.outside,
  // cleaner and easier to read
})}
```

Additional recommendations:
- Use Tailwind classes instead of inline styles (e.g., use `touch-manipulation` instead of `style={{ touchAction: "manipulation" }}`)
- Use standard classes like `rounded-md` instead of inline styles for border radius
- For text alignment that respects RTL languages, use `text-start` rather than `text-left`
- Maintain consistent class ordering, with structural classes first, followed by visual styles

These practices make your code more maintainable, easier to review, and better for internationalization.