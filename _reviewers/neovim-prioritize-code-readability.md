---
title: prioritize code readability
description: Write code that prioritizes readability and clarity over brevity. Use
  proper formatting, clear expressions, and consistent patterns to make code easier
  to understand and maintain.
repository: neovim/neovim
label: Code Style
language: Other
comments_count: 6
repository_stars: 91433
---

Write code that prioritizes readability and clarity over brevity. Use proper formatting, clear expressions, and consistent patterns to make code easier to understand and maintain.

Key practices:
- Use string.format() for multiple concatenations instead of .. operators: `('Updated state to `%s` in `%s`'):format(version_str, name)` instead of `'Updated state to `' .. version_str .. '` in `' .. name .. '`'`
- Add parentheses to complex boolean expressions for clarity: `(metadata.conceal ~= nil) and metadata.conceal or (metadata[capture] and metadata[capture].conceal)` instead of `metadata.conceal ~= nil and metadata.conceal or metadata[capture] and metadata[capture].conceal`
- Put boolean variables directly in conditions rather than comparing to true/false: `if status then` instead of `if status == true then`
- Break complex declarations/assignments when they involve complex expressions: separate `local version_str = resolve_version()` and `local version_ref = get_reference()` instead of `local version_str, version_ref = resolve_version(), get_reference()`
- Use reasonable line length limits (120 characters) to avoid unnecessary line breaks that hurt readability
- Choose descriptive variable names and clear control flow patterns that make the code's intent obvious

The goal is to write code that another developer can quickly understand without having to parse complex expressions or guess at intentions.