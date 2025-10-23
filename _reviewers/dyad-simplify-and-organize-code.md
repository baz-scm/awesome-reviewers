---
title: Simplify and organize code
description: Keep code simple, direct, and well-organized by avoiding unnecessary
  complexity and properly structuring components. Remove redundant implementations
  when existing mechanisms already handle the functionality. Avoid indirect approaches
  when more straightforward solutions exist. Extract large components into separate
  files when they become unwieldy.
repository: dyad-sh/dyad
label: Code Style
language: TSX
comments_count: 3
repository_stars: 16903
---

Keep code simple, direct, and well-organized by avoiding unnecessary complexity and properly structuring components. Remove redundant implementations when existing mechanisms already handle the functionality. Avoid indirect approaches when more straightforward solutions exist. Extract large components into separate files when they become unwieldy.

Examples of improvements:
- Remove unnecessary IPC calls when existing update mechanisms already handle the functionality (like using `updateSettings` instead of additional `setNodePath` calls)
- Use direct attribute mapping instead of indirect conditional logic (e.g., `attributes.type` mapped to `id` rather than complex conditional chains)
- Extract substantial component logic into separate files when components become too large (like Azure-specific configuration logic)

This approach improves code readability, reduces maintenance burden, and makes the codebase more intuitive for other developers to understand and modify.