---
title: Optional dependency management
description: Avoid including optional or provider-specific dependencies in the main
  dependency list. Dependencies should only be required if they are essential for
  core functionality that all users need.
repository: stanfordnlp/dspy
label: Configurations
language: Toml
comments_count: 4
repository_stars: 27813
---

Avoid including optional or provider-specific dependencies in the main dependency list. Dependencies should only be required if they are essential for core functionality that all users need.

Make dependencies optional when they are:
- Provider-specific (e.g., groq, mistralai, anthropic clients)
- Feature-specific (e.g., mcp for specific Python versions)
- Test-only requirements that not all developers need

Use the `optional = true` flag and organize them into appropriate extras groups:

```toml
[tool.poetry.dependencies]
# Core dependencies only
python = ">=3.9,<3.12"
pydantic = "^2.0"

# Optional dependencies
groq = { version = "^0.4.2", optional = true }
mistralai = { version = "^0.1.3", optional = true }

[tool.poetry.extras]
groq = ["groq"]
mistral = ["mistralai"]
```

This approach prevents forcing unnecessary installations on users who don't need specific providers or features, while still making them available for those who do.