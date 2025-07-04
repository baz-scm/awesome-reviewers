---
title: Maintain consistent naming
description: 'Ensure naming follows consistent patterns throughout the codebase in
  both style and structure:


  1. Use agreed-upon case style for identifiers (e.g., snake_case for functions):'
repository: zed-industries/zed
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 62119
---

Ensure naming follows consistent patterns throughout the codebase in both style and structure:

1. Use agreed-upon case style for identifiers (e.g., snake_case for functions):
```diff
- {{# if (hasTool 'grep') }}
+ {{# if (has_tool 'grep') }}
```

2. Maintain consistent ordering in hierarchical names, with namespaces coming first:
```diff
- export additional-language-server-workspace-configuration: func(...)
+ export language-server-additional-workspace-configuration: func(...)
```

3. For selectors and hierarchical identifiers, order components from less specific to more specific:
```diff
- (emphasis) @markup.emphasis
+ (emphasis) @emphasis.markup
```

This consistency improves code readability, makes the codebase more predictable, and reduces cognitive load when writing or reviewing code.