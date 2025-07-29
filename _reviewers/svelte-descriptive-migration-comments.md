---
title: Descriptive migration comments
description: When adding migration task comments, always include specific details
  about why manual intervention is required rather than using generic instructions.
  This helps developers understand the underlying issue and implement the correct
  fix more efficiently.
repository: sveltejs/svelte
label: Migrations
language: Other
comments_count: 3
repository_stars: 83580
---

When adding migration task comments, always include specific details about why manual intervention is required rather than using generic instructions. This helps developers understand the underlying issue and implement the correct fix more efficiently.

Migration comments should explain the root cause of the migration failure, such as invalid identifiers, syntax conflicts, or breaking changes. This context is crucial for successful manual migration.

Example:
```html
<!-- Bad: Generic comment -->
<!-- @migration-task: migrate this slot by hand -->

<!-- Good: Specific comment with reason -->
<!-- @migration-task: migrate this slot by hand, `cool:stuff` is an invalid identifier -->
<!-- @migration-task: migrate this slot by hand, `cool stuff` is an invalid identifier -->
```

The specific reason helps developers immediately understand what needs to be fixed - in this case, slot names containing colons or spaces that are not valid identifiers in the new syntax.