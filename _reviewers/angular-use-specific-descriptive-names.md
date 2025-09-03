---
title: Use specific descriptive names
description: Choose specific, meaningful names that clearly communicate purpose rather
  than generic or ambiguous alternatives. This applies to classes, methods, variables,
  and examples in documentation.
repository: angular/angular
label: Naming Conventions
language: Markdown
comments_count: 4
repository_stars: 98611
---

Choose specific, meaningful names that clearly communicate purpose rather than generic or ambiguous alternatives. This applies to classes, methods, variables, and examples in documentation.

For component classes, follow established naming conventions by removing unnecessary suffixes when they don't add semantic value. For method names, select terms that clearly indicate functionality without creating confusion about the underlying implementation or capabilities.

In examples and documentation, prefer descriptive names that reflect the actual use case rather than generic placeholders.

**Examples:**

```ts
// Prefer specific over generic
export class CharacterViewer { } // instead of AppComponent
export class UserDetail { }      // instead of UserDetailComponent

// Choose clear, unambiguous method names  
stream: ({userId}) => this.userData.load(userId),  // instead of fetch()

// Use semantically accurate variable names
request: ({value}) => `/api/check-username?${value()}`, // correct signal usage
```

This practice improves code readability, reduces cognitive load, and helps other developers quickly understand the purpose and scope of different code elements.