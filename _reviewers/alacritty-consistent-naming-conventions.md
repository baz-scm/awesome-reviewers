---
title: Consistent naming conventions
description: Maintain consistent naming patterns and capitalization throughout the
  codebase, especially for configuration options, string values, and identifiers.
  This includes using consistent capitalization for similar values (e.g., "None" instead
  of mixing "none" and "None"), adopting uniform naming patterns for related options
  (e.g., using "duration" consistently...
repository: alacritty/alacritty
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 59675
---

Maintain consistent naming patterns and capitalization throughout the codebase, especially for configuration options, string values, and identifiers. This includes using consistent capitalization for similar values (e.g., "None" instead of mixing "none" and "None"), adopting uniform naming patterns for related options (e.g., using "duration" consistently instead of verbose alternatives like "fade_time_in_secs"), and ensuring clear, consistent prefixes or patterns for grouped identifiers.

For example, instead of mixing capitalization:
```
# Inconsistent
*line_indicator* { foreground = "none", background = "none" }
*decorations* "Full" | "None" | "Transparent"

# Consistent  
*line_indicator* { foreground = "None", background = "None" }
*decorations* "Full" | "None" | "Transparent"
```

Similarly, prefer concise, consistent naming over verbose alternatives:
```
# Verbose and inconsistent
*fade_time_in_secs* <float>

# Concise and consistent with other duration options
*duration* <integer>
```

This approach reduces cognitive load, prevents confusion, and makes the codebase more maintainable by establishing predictable naming patterns that developers can rely on.