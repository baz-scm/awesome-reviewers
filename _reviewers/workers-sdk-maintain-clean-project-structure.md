---
title: maintain clean project structure
description: Keep your codebase organized and clutter-free by removing unnecessary
  files, directories, and artifacts that serve no functional purpose. When tools have
  compatibility issues with certain file types, configure appropriate ignore patterns
  rather than leaving problematic files to cause confusion or errors.
repository: cloudflare/workers-sdk
label: Code Style
language: Other
comments_count: 2
repository_stars: 3379
---

Keep your codebase organized and clutter-free by removing unnecessary files, directories, and artifacts that serve no functional purpose. When tools have compatibility issues with certain file types, configure appropriate ignore patterns rather than leaving problematic files to cause confusion or errors.

Examples of maintaining clean structure:
- Remove empty directories with .gitkeep files when they're no longer needed
- Add problematic file types to tool ignore files (e.g., .prettierignore for .d.ts files that cause parsing errors)
- Question whether directories and files are actually necessary before adding them to the project

This practice reduces cognitive load for developers, prevents confusion about project structure, and ensures that development tools work reliably without encountering parsing or processing errors.