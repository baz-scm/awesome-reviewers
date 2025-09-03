---
title: minimize core dependencies
description: Keep core dependencies minimal in configuration files like pyproject.toml.
  Non-essential packages should be added as optional dependencies or placed in extras
  sections rather than as required core dependencies. This prevents package bloat
  and allows users to install only what they need.
repository: BerriAI/litellm
label: Configurations
language: Toml
comments_count: 3
repository_stars: 28310
---

Keep core dependencies minimal in configuration files like pyproject.toml. Non-essential packages should be added as optional dependencies or placed in extras sections rather than as required core dependencies. This prevents package bloat and allows users to install only what they need.

When adding new dependencies, first determine if they are truly required for core functionality. If the dependency is only needed for specific features, testing, or optional functionality, use the appropriate configuration section:

```toml
# Core dependencies - only essential packages
[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.28.0"

# Optional dependencies for specific features
[tool.poetry.extras]
rich-output = ["rich>=13.0.0"]
anthropic-support = ["anthropic^0.50.0"]

# Development/testing dependencies
[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
```

This approach maintains a lean core package while providing flexibility for users who need additional functionality.