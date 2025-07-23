---
title: Clean code formatting rules
description: 'Maintain consistent and clean code formatting to improve readability
  and maintainability. Follow these guidelines:


  1. Use correct syntax for utility classes:'
repository: continuedev/continue
label: Code Style
language: TSX
comments_count: 7
repository_stars: 27819
---

Maintain consistent and clean code formatting to improve readability and maintainability. Follow these guidelines:

1. Use correct syntax for utility classes:
   ```tsx
   // ❌ Bad
   className="gap 1.5 flex-row"
   className={`${toolsSupported ? "md:flex" : "int:flex"} hover:underline"`}
   
   // ✅ Good
   className="gap-1.5 flex-row"
   className={`hover:underline ${toolsSupported ? "md:flex" : ""}`}
   ```

2. Keep class strings organized and manageable:
   - Extract complex conditional classes into variables
   - Use template literals for dynamic classes
   - Maintain consistent ordering (layout → spacing → visual)

3. Avoid inline comments in expressions:
   ```tsx
   // ❌ Bad
   ) : item.message.role === "tool" ? null : item.message.role === // comment here
   
   // ✅ Good
   // Comment above the expression
   ) : item.message.role === "tool" ? null : item.message.role === "assistant"
   ```

4. Use appropriate import paths:
   - Import from main module exports rather than internal files
   - Maintain proper encapsulation of implementation details
   - Keep imports organized and grouped by type

These rules help maintain code consistency, improve readability, and make the codebase easier to maintain and refactor.