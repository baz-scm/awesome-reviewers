---
title: maintain consistent style
description: Ensure consistent application of coding style conventions throughout
  the codebase, including naming patterns, type usage, code organization, and formatting
  standards.
repository: angular/angular
label: Code Style
language: TypeScript
comments_count: 12
repository_stars: 98611
---

Ensure consistent application of coding style conventions throughout the codebase, including naming patterns, type usage, code organization, and formatting standards.

Key areas to maintain consistency:

**Naming Conventions:**
- Use consistent casing for constants (e.g., `STACKOVERFLOW` not `StackOverflow`)
- Remove underscore prefixes from private members as per current standards
- Apply `readonly` modifier consistently to input signals and computed values

**Type Usage:**
- Prefer `unknown` over `any` for better type safety
- Use consistent patterns for optional chaining and type assertions

**Code Organization:**
- Place documentation comments before decorators consistently
- Extract repeated constants to the top of files or shared utilities
- Use `async/await` syntax consistently instead of `Promise.resolve()`

**Example of consistent readonly usage:**
```typescript
// Consistent - all inputs marked as readonly
readonly docContent = input<DocContent | undefined>();
readonly urlFragment = toSignal(this.route.fragment);
readonly hasClosed = linkedSignal(() => { ... });

// Inconsistent - missing readonly modifiers
docContent = input<DocContent | undefined>();
urlFragment = toSignal(this.route.fragment);
```

**Example of consistent constant extraction:**
```typescript
// Good - constants extracted and consistently named
const MAX_DISPLAY_LENGTH = 200;
const COPY_FEEDBACK_TIMEOUT = 2000;
const STACKOVERFLOW = 'https://stackoverflow.com/questions/tagged/angular';

// Avoid - magic numbers and inconsistent naming
setTimeout(() => { ... }, 2000);
export const StackOverflow = 'https://stackoverflow.com/questions/tagged/angular';
```

Consistency in style reduces cognitive load, improves maintainability, and makes the codebase more professional. Establish team conventions and apply them uniformly across all files.