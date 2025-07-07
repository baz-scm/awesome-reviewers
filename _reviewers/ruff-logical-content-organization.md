---
title: Logical content organization
description: Organize code and documentation logically based on functionality and
  dependencies. Place files in directories that reflect their purpose rather than
  superficial characteristics. Structure documentation so prerequisite concepts appear
  before concepts that depend on them.
repository: astral-sh/ruff
label: Code Style
language: Markdown
comments_count: 2
repository_stars: 40619
---

Organize code and documentation logically based on functionality and dependencies. Place files in directories that reflect their purpose rather than superficial characteristics. Structure documentation so prerequisite concepts appear before concepts that depend on them.

For example:
- Test files should be placed in directories matching their core functionality (e.g., tests for special-cased functions should go in the appropriate special-case directory, not in unrelated directories)
- Documentation sections should be ordered so that foundational concepts are introduced first, especially when other sections build upon them (e.g., putting the "Callable" section before "Tuple" when callable arguments are used to demonstrate contravariant contexts)

This organizational approach improves readability, makes the codebase more intuitive to navigate, and helps developers understand relationships between different components.