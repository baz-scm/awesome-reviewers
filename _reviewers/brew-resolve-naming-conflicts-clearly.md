---
title: Resolve naming conflicts clearly
description: 'When naming components, packages, or files that conflict with existing
  names in your system or related ecosystems, follow a systematic approach to ensure
  uniqueness while maintaining semantic clarity:'
repository: Homebrew/brew
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 44168
---

When naming components, packages, or files that conflict with existing names in your system or related ecosystems, follow a systematic approach to ensure uniqueness while maintaining semantic clarity:

1. First attempt: Prepend the vendor or developer name followed by a hyphen
   ```
   # Instead of just:
   unison.rb
   
   # Use:
   panic-unison.rb
   ```

2. If conflicts persist: Add descriptive suffixes that clarify the purpose or nature of the item
   ```
   # For different implementations of the same concept:
   appium (formula)
   appium-desktop (cask)
   
   # For application variants:
   angband (formula)
   angband-app (cask)
   ```

3. Maintain consistency with naming conventions in other systems (e.g., other package managers) when your component exists across multiple ecosystems, making only minimal adjustments required by your specific naming conventions.

This approach ensures names remain unique, descriptive, and intuitive, making the codebase more maintainable and reducing confusion for developers working across related systems.