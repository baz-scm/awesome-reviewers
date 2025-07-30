---
title: Ensure semantic naming clarity
description: Names should clearly communicate their actual behavior and preserve sufficient
  context for meaningful identification. For functions with conditional behavior,
  use descriptive suffixes like `_if_needed` or `_maybe` to indicate optionality.
  For paths and identifiers, maintain enough context to ensure usability - avoid over-shortening
  that removes essential...
repository: smallcloudai/refact
label: Naming Conventions
language: Rust
comments_count: 2
repository_stars: 3114
---

Names should clearly communicate their actual behavior and preserve sufficient context for meaningful identification. For functions with conditional behavior, use descriptive suffixes like `_if_needed` or `_maybe` to indicate optionality. For paths and identifiers, maintain enough context to ensure usability - avoid over-shortening that removes essential information.

Examples:
- Instead of `wait_for_indexing()` for conditional waiting, use `wait_for_indexing_if_needed()`
- Instead of shortening `/home/user/work/dir1/file.ext` to just `file.ext`, preserve context as `dir1/file.ext`

This ensures that names serve as clear documentation of intent and maintain practical usability for developers and tools.