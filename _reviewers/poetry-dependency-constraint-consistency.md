---
title: dependency constraint consistency
description: Maintain consistent formatting and rationale for dependency version constraints
  in configuration files. Use caret notation (`^1.0.0`) instead of range notation
  (`>=1,<2`) for cleaner syntax when specifying compatible version ranges. When constraining
  to specific Python versions, choose between explicit version strings (`"3.7"`) and
  comparison operators...
repository: python-poetry/poetry
label: Configurations
language: Toml
comments_count: 7
repository_stars: 33496
---

Maintain consistent formatting and rationale for dependency version constraints in configuration files. Use caret notation (`^1.0.0`) instead of range notation (`>=1,<2`) for cleaner syntax when specifying compatible version ranges. When constraining to specific Python versions, choose between explicit version strings (`"3.7"`) and comparison operators (`"<3.8"`) based on maintainability - use explicit versions when targeting a single version for easier removal later, and comparison operators for broader compatibility ranges.

For critical dependencies, document the reasoning behind constraint choices. Exact pinning should be intentional and documented (e.g., "We pin poetry-core exactly since Poetry 1.3 because we release Poetry for every poetry-core bugfix"). Avoid yanked versions by checking package status before updating constraints.

Example:
```toml
# Preferred: caret notation for compatible ranges
requests-toolbelt = "^1.0.0"

# Avoid: range notation
requests-toolbelt = ">=1,<2"

# Explicit version for single-version targeting (easier to grep/remove)
"backports.cached-property" = { version = "^1.0.2", python = "3.7" }

# Comparison for broader compatibility
importlib-metadata = { version = "^4.4", python = "<3.10" }
```

This ensures configuration files are maintainable, constraints are intentional, and version specifications follow consistent patterns across the project.