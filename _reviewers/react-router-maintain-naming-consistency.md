---
title: maintain naming consistency
description: Ensure consistent naming conventions across the entire codebase, including
  terminology, file names, directory structures, and API naming. Inconsistent naming
  creates confusion and poor developer experience.
repository: remix-run/react-router
label: Naming Conventions
language: Markdown
comments_count: 5
repository_stars: 55270
---

Ensure consistent naming conventions across the entire codebase, including terminology, file names, directory structures, and API naming. Inconsistent naming creates confusion and poor developer experience.

Key areas to maintain consistency:

**Terminology**: Use the same terms consistently across code, documentation, and templates. For example, choose either "browser" or "client" and use it consistently throughout the codebase rather than mixing terms.

**Directory/File Naming**: Maintain consistent naming patterns across templates, examples, and documentation. If using `app/routes/` in templates, use the same structure in tutorials and examples rather than switching to `app/pages/`.

**API Documentation**: Follow consistent naming patterns for documentation files, especially for unstable APIs. For example, consistently handle unstable API documentation naming to maintain stable URLs.

**File Naming**: Use descriptive, specific names rather than generic ones. Instead of `file-storage.server.ts`, use `avatar-storage.server.ts` to clearly indicate the file's purpose.

Example of inconsistent naming to avoid:
```tsx
// Documentation uses "browser" 
entry.browser.tsx

// But code comments refer to "client"
// This is the client entry point...

// Templates use different directory names
app/routes/contact.tsx  // in one template
app/pages/contact.tsx   // in another template
```

Before introducing new naming conventions, audit existing patterns and align with established conventions. When changes are necessary, update all related files, documentation, and examples simultaneously to maintain consistency.