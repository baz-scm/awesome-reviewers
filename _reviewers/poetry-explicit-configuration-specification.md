---
title: explicit configuration specification
description: Always explicitly specify configuration values rather than relying on
  defaults or implicit behavior. Poetry requires unambiguous configuration to function
  correctly, and many issues arise from incomplete or assumed specifications.
repository: python-poetry/poetry
label: Configurations
language: Markdown
comments_count: 9
repository_stars: 33496
---

Always explicitly specify configuration values rather than relying on defaults or implicit behavior. Poetry requires unambiguous configuration to function correctly, and many issues arise from incomplete or assumed specifications.

Key areas requiring explicit specification:

**Version Constraints**: Explicitly declare Python version requirements and dependency constraints. If using both `project.requires-python` and `tool.poetry.dependencies.python`, ensure the Poetry specification is a subset of the project specification.

```toml
[project]
requires-python = ">=3.8"

[tool.poetry.dependencies]
python = "^3.8"  # Must be subset of project.requires-python

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]  # Include version constraints
```

**Build Dependencies**: Assume only Python built-ins are available in build environments. Explicitly declare all required packages, including common ones like `setuptools`.

```toml
[build-system]
requires = ["poetry-core", "setuptools", "cython"]  # Don't assume setuptools is available
```

**Repository Sources**: Explicitly configure package source priorities and constraints to avoid dependency confusion attacks. Omit URLs for PyPI when configuring it explicitly.

```toml
[[tool.poetry.source]]
name = "pypi"
priority = "primary"  # No URL needed for PyPI

[[tool.poetry.source]]
name = "private-repo"
url = "https://private.example.com/simple/"
priority = "explicit"
```

**CLI Usage**: Use `--` to terminate option parsing when values might start with hyphens, and specify full paths or explicit options rather than relying on defaults.

```bash
poetry config http-basic.repo token -- ${TOKEN}  # Prevent parsing issues
```

This approach prevents configuration ambiguity, reduces debugging time, and ensures consistent behavior across different environments and Poetry versions.