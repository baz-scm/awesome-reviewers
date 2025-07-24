---
title: Consistent naming patterns
description: Maintain consistent naming conventions throughout the codebase to improve
  readability and maintainability. This applies to translation keys, command names,
  variables, and terminology.
repository: n8n-io/n8n
label: Naming Conventions
language: Json
comments_count: 4
repository_stars: 122978
---

Maintain consistent naming conventions throughout the codebase to improve readability and maintainability. This applies to translation keys, command names, variables, and terminology.

For translation keys:
- Choose one style (camelCase, snake_case, or dot notation) and apply it consistently
- Avoid mixing styles like `dataStore.tab.label` with `data.store.empty.label` or `contextMenu.FilterExecutionsBy` with references to `contextMenu.filter_executions_by`

For command and function names:
- Name should clearly reflect the actual purpose and behavior
- For example, use `test:e2e` or `test:playwright` instead of the ambiguous `test:docker` if the command runs playwright tests
- Use `test:show:report` instead of `test:report` to clarify the action being performed

For terminology:
- Use consistent terms for the same concepts throughout the application
- Avoid replacing established terms (like changing 'workflow' to 'automation sequence') without updating all references

Consistency in naming reduces cognitive load for developers, prevents bugs from mismatched references, and makes the codebase more maintainable over time.