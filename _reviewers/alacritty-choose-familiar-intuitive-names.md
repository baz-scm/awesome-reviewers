---
title: Choose familiar, intuitive names
description: When naming variables, methods, or configuration options, prioritize
  terms that are both intuitive to users and familiar within the relevant domain.
  Avoid technical jargon when simpler, more natural alternatives exist, while also
  preferring established terminology that the target audience already knows.
repository: alacritty/alacritty
label: Naming Conventions
language: Yaml
comments_count: 3
repository_stars: 59675
---

When naming variables, methods, or configuration options, prioritize terms that are both intuitive to users and familiar within the relevant domain. Avoid technical jargon when simpler, more natural alternatives exist, while also preferring established terminology that the target audience already knows.

For user-facing actions, choose verbs that clearly communicate the intended behavior. For example, prefer "Create" over "Spawn" for window operations, as "create" is more natural and immediately understandable to users.

For domain-specific concepts, use well-established terminology that practitioners in that field would recognize. For instance, in terminal emulators, use "inverse" rather than "opposing" when referring to swapped foreground/background colors, since "inverse text" is the standard term.

Example:
```yaml
# Preferred - uses natural, domain-appropriate language
- CreateNewWindow    # intuitive action verb
- inverse_colors     # established terminal terminology

# Avoid - technical jargon or non-standard terms  
- SpawnNewWindow     # technical but less intuitive
- opposing_colors    # generic but not domain-standard
```

This approach ensures that names are both accessible to users and technically precise within the relevant context.