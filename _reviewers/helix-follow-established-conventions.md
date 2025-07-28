---
title: Follow established conventions
description: Configuration settings should align with official language documentation
  and established community standards rather than arbitrary personal preferences.
  This applies to indentation styles, formatter configurations, and syntax requirements.
repository: helix-editor/helix
label: Code Style
language: Toml
comments_count: 5
repository_stars: 39026
---

Configuration settings should align with official language documentation and established community standards rather than arbitrary personal preferences. This applies to indentation styles, formatter configurations, and syntax requirements.

For language-specific settings, consult official documentation:
- Use 2 spaces for Typst indentation as specified in official docs, not 4
- Follow PEP 8 for Python when setting required indentation
- Only enable auto-format when it's standard practice for the language

For tool configurations, ensure commands and arguments are syntactically correct:
```toml
# Correct formatter configurations
formatter = { command = "prettier", args = ["--parser", "typescript"] }
formatter = { command = "biome", args = ["format", "--stdin-file-path=a.js"] }
formatter = { command = "deno", args = ["fmt", "--ext", "js"] }

# Use full 6-character hex codes, not 3-character shortcuts
"ui.background" = { bg = "#262335" }  # not "#263"
```

This ensures consistency with ecosystem expectations and prevents configuration errors that could break functionality.