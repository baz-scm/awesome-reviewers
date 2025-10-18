---
title: Use descriptive specific names
description: Choose names that clearly communicate purpose and scope rather than generic
  or overly broad terms. Names should be specific enough to accommodate future variants
  and descriptive enough to indicate their function without requiring additional context.
repository: sst/opencode
label: Naming Conventions
language: Go
comments_count: 3
repository_stars: 28213
---

Choose names that clearly communicate purpose and scope rather than generic or overly broad terms. Names should be specific enough to accommodate future variants and descriptive enough to indicate their function without requiring additional context.

Avoid generic package names like "util" in favor of descriptive ones that indicate the specific functionality. When naming themes, configurations, or variants, include distinguishing characteristics to prevent conflicts with future additions.

Examples:
- Instead of `RegisterTheme("catppuccin", ...)` use `RegisterTheme("catppuccin-mocha", ...)` to accommodate other Catppuccin variants
- Instead of `util.NewFocusTracker()` use `focus.NewTracker()` where the package name describes its purpose
- Extract reusable naming maps (like provider labels) to shared locations rather than duplicating them across components

This approach improves code maintainability, reduces naming conflicts, and makes the codebase more self-documenting.