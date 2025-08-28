---
title: Use descriptive names
description: Choose clear, descriptive names for variables, methods, types, and parameters
  that unambiguously convey their purpose and avoid conflicts. Prefer full words over
  abbreviations and ensure names are specific enough to prevent clashes with inherited
  or similar functionality.
repository: cloudflare/agents
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 2312
---

Choose clear, descriptive names for variables, methods, types, and parameters that unambiguously convey their purpose and avoid conflicts. Prefer full words over abbreviations and ensure names are specific enough to prevent clashes with inherited or similar functionality.

Examples of improvements:
- Use `options` instead of `opts` for better clarity
- Use `TransportType` instead of `Protocol` when the term "protocol" is overloaded in the domain
- Use `onMcpError` instead of `onError` to avoid conflicts with base class methods

This practice reduces cognitive load, prevents naming conflicts during inheritance or composition, and makes code more maintainable by clearly expressing intent through naming.