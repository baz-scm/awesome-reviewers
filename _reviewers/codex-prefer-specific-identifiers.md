---
title: Prefer specific identifiers
description: Always use specific, descriptive names for identifiers rather than generic
  terms. Names should clearly indicate their purpose and context, making code more
  readable and self-documenting. This applies to variables, parameters, types, and
  files.
repository: openai/codex
label: Naming Conventions
language: TypeScript
comments_count: 4
repository_stars: 31275
---

Always use specific, descriptive names for identifiers rather than generic terms. Names should clearly indicate their purpose and context, making code more readable and self-documenting. This applies to variables, parameters, types, and files.

Examples:
- Use `mcpServers` instead of `servers` to include context
- Prefer `storeResponses` over `store` to clarify the parameter's purpose
- Name types specifically like `UpdateState` instead of generic `State`
- Use file names that reflect content purpose (e.g., `update-state.json`, `.codex.env`)

This practice reduces cognitive load for other developers, improves maintainability, and helps prevent confusion or misuse of code elements. The additional verbosity is well worth the clarity it provides.