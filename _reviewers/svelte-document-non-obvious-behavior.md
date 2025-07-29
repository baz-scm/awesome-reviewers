---
title: Document non-obvious behavior
description: Write documentation that explains behavior and context that may not be
  obvious to newcomers, even if it seems clear to experienced developers. Include
  explanations for domain-specific concepts, data structure representations, and implicit
  behaviors that could confuse someone unfamiliar with the codebase.
repository: sveltejs/svelte
label: Documentation
language: TypeScript
comments_count: 2
repository_stars: 83580
---

Write documentation that explains behavior and context that may not be obvious to newcomers, even if it seems clear to experienced developers. Include explanations for domain-specific concepts, data structure representations, and implicit behaviors that could confuse someone unfamiliar with the codebase.

For example, when documenting complex data structures, explain what arrays represent and why certain design decisions were made:

```typescript
/**
 * Quoted/string values are represented by an array, even if they contain 
 * a single expression like `"{x}"`, since they may be a combination of 
 * text and expression values such as `style="color: {color} !important"`.
 */
value: Array<Text | ExpressionTag> | true;
```

Rather than assuming knowledge, provide context that helps developers understand the reasoning behind the implementation. What feels obvious after working with a codebase for months may be completely unclear to someone encountering it for the first time.