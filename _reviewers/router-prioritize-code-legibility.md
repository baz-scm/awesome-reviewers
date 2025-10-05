---
title: Prioritize code legibility
description: Write clear, explicit code that prioritizes readability over brevity.
  Remove unnecessary operations and use straightforward syntax patterns. This is especially
  important in library code where clarity benefits all consumers.
repository: TanStack/router
label: Code Style
language: TSX
comments_count: 2
repository_stars: 11590
---

Write clear, explicit code that prioritizes readability over brevity. Remove unnecessary operations and use straightforward syntax patterns. This is especially important in library code where clarity benefits all consumers.

Key practices:
- Eliminate redundant operations (like unnecessary object spreading of rest parameters)
- Use explicit syntax over implicit shortcuts
- Structure code for maximum legibility

Example of improvement:
```javascript
// Avoid: Unnecessary spreading of rest object
).map(({ children, ...style }) => ({
  tag: 'style',
  attrs: {
    ...style,
  },

// Prefer: Direct use of rest parameter
).map(({ children, ...attrs }) => ({
  tag: 'style',
  attrs,

// Avoid: Implicit returns with complex logic
.handler(async ({ data: { name, age, pets } }) => 
  `Hello, ${name}! You are ${age + testValues.__adder} years old, and your favourite pets are ${pets.join(',')}.`
)

// Prefer: Explicit returns with clear structure
.handler(({ data: { name, age, pets } }) => {
  return `Hello, ${name}! You are ${age + testValues.__adder} years old, and your favourite pets are ${pets.join(',')}.`
})
```

The goal is legibility - code should be immediately understandable to any developer reading it.