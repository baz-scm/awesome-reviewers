---
title: avoid problematic identifier names
description: Choose identifier names that avoid system compatibility issues and follow
  proper naming conventions. Avoid reserved words, system-problematic names, and invalid
  characters that can cause issues across different platforms or violate language
  standards.
repository: smallcloudai/refact
label: Naming Conventions
language: Python
comments_count: 2
repository_stars: 3114
---

Choose identifier names that avoid system compatibility issues and follow proper naming conventions. Avoid reserved words, system-problematic names, and invalid characters that can cause issues across different platforms or violate language standards.

Key guidelines:
- Avoid names that conflict with system reserved words (e.g., "aux" causes issues on Windows)
- Restrict identifiers to safe character sets (alphanumeric, underscores, hyphens where appropriate)
- Exclude spaces and special characters that may not be universally supported
- Use full descriptive names instead of abbreviated forms that might conflict with system names

Example from the codebase:
```python
# Problematic - 'aux' is reserved on Windows
from self_hosting_machinery.finetune.scripts.aux.finetune_filter_status_tracker import FinetuneFilterStatusTracker

# Better - use full descriptive name
from self_hosting_machinery.finetune.scripts.auxiliary.finetune_filter_status_tracker import FinetuneFilterStatusTracker

# Problematic - spaces in identifier validation
if not re.match("^[a-zA-Z0-9_ -]*$", v):

# Better - exclude spaces from allowed characters
if not re.match("^[a-zA-Z0-9_-]*$", v):
```

This prevents deployment issues, ensures cross-platform compatibility, and maintains consistent identifier standards across the codebase.