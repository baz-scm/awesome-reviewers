---
title: consistent descriptive naming
description: Maintain consistent naming patterns across similar functionality while
  ensuring names accurately describe their current purpose and scope. When multiple
  options exist for the same feature, standardize on one clear option to avoid confusion
  in documentation and usage. Update variable names when their type or purpose changes,
  and use descriptive names that...
repository: cypress-io/cypress
label: Naming Conventions
language: JavaScript
comments_count: 5
repository_stars: 48850
---

Maintain consistent naming patterns across similar functionality while ensuring names accurately describe their current purpose and scope. When multiple options exist for the same feature, standardize on one clear option to avoid confusion in documentation and usage. Update variable names when their type or purpose changes, and use descriptive names that clearly indicate scope and function.

Examples:
- Standardize on `--component` instead of supporting both `--component` and `--ct` flags
- Rename `written` to `writtenChunkCount` when changing from boolean to counter
- Use consistent namespacing like `/__cypress/bundled` to match existing conventions
- Name debug variables consistently as `debugVerbose` even when no non-verbose version exists
- Update labels like "All Specs" to "All Integration Specs" when context requires specificity

This prevents inconsistent documentation, reduces cognitive load for developers, and ensures the codebase remains predictable and maintainable.