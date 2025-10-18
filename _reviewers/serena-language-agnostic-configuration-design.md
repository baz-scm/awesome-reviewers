---
title: Language-agnostic configuration design
description: Design configuration parameters to be language-agnostic when possible,
  use established configuration objects, and maintain consistency across language
  server implementations. Avoid language-specific CLI options or constructor parameters
  when the functionality could apply broadly.
repository: oraios/serena
label: Configurations
language: Python
comments_count: 7
repository_stars: 14465
---

Design configuration parameters to be language-agnostic when possible, use established configuration objects, and maintain consistency across language server implementations. Avoid language-specific CLI options or constructor parameters when the functionality could apply broadly.

Key principles:
1. **Use enum values instead of class names** for language server-specific settings to make them user-friendly
2. **Make CLI options generic** - use `--ls-max-memory` instead of `--max-memory` for Intelephense-specific features
3. **Leverage existing configuration objects** like `LanguageServerConfig` instead of adding new constructor parameters
4. **Handle configuration evolution properly** - force user decisions on new settings rather than assuming defaults, and provide clear error messages for missing required keys

Example of good configuration design:
```python
# Good: Use enum value for LS-specific settings
custom_settings = self._solidlsp_settings.ls_specifics.get("intelephense", {})

# Good: Generic CLI option that could apply to multiple language servers  
@click.option("--ls-max-memory", type=int, help="Maximum memory (MB) for language server")

# Good: Use existing config object
def __init__(self, config: LanguageServerConfig, logger: LanguageServerLogger, ...):
    max_memory = config.max_memory  # Instead of separate parameter

# Good: Force user decision on new config
if "ignore_all_files_in_gitignore" not in config_dict:
    raise ValueError("Missing required config: ignore_all_files_in_gitignore")
```

This approach ensures configuration remains maintainable, user-friendly, and consistent as the codebase grows across multiple language servers.