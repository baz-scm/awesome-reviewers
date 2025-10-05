---
title: Tool-specific configuration compatibility
description: When working with configuration files that support multiple tools or
  package managers, ensure that configuration syntax and constraints accommodate all
  supported tools while maintaining functionality across the ecosystem.
repository: commaai/openpilot
label: Configurations
language: Toml
comments_count: 4
repository_stars: 58214
---

When working with configuration files that support multiple tools or package managers, ensure that configuration syntax and constraints accommodate all supported tools while maintaining functionality across the ecosystem.

Different tools have specific requirements and limitations that must be understood and accommodated. For example, uv requires lower bounds for dependencies in preview mode ("sounddevice >= 0" instead of "sounddevice"), cannot combine github sources with platform markers in the same declaration, and poetry has limitations on non-existent version specifications.

Always verify that configuration changes work across all intended tools and document tool-specific constraints when they influence configuration decisions. For static analysis tools like mypy, align version settings with the project's minimum supported version rather than the latest available version to prevent use of unsupported language features.

Example from pyproject.toml:
```toml
# uv requires lower bounds in preview mode
"sounddevice >= 0",  # micd + soundd

# uv limitation: github source + markers must be split
dependencies = [
    "metadrive-simulator; platform_machine != 'aarch64'"
]
[tool.uv.sources]
metadrive-simulator = { git = "https://github.com/commaai/metadrive.git", branch = "python3.12" }

# mypy should target minimum supported Python version
[tool.mypy]
python_version = "3.11"  # keep to minimum supported, not latest
```