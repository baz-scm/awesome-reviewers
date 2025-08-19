---
title: prefer CSS over JavaScript
description: Use CSS solutions instead of JavaScript state management for simple styling
  and interactions. This approach improves maintainability, reduces complexity, and
  follows web standards best practices.
repository: microsoft/playwright
label: Code Style
language: TSX
comments_count: 3
repository_stars: 76113
---

Use CSS solutions instead of JavaScript state management for simple styling and interactions. This approach improves maintainability, reduces complexity, and follows web standards best practices.

Examples of when to apply this:
- Use CSS `:hover` pseudo-classes instead of `onMouseEnter`/`onMouseLeave` event handlers
- Implement show/hide behavior with CSS `display` or `visibility` properties rather than React state
- Apply styling through CSS classes instead of inline styles

Example transformation:
```tsx
// Instead of JavaScript state management:
const [isOpen, setIsOpen] = useState(false);
return (
  <div onMouseEnter={() => setIsOpen(true)} onMouseLeave={() => setIsOpen(false)}>
    {isOpen && <div className="dropdown-menu">...</div>}
  </div>
);

// Use CSS-based solution:
return (
  <div className="dropdown">
    <div className="dropdown-menu">...</div>
  </div>
);

/* CSS */
.dropdown:not(:hover) .dropdown-menu {
  display: none;
}
```

This approach reduces JavaScript complexity, improves performance, and makes the code more maintainable by leveraging native browser capabilities.