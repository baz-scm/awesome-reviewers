---
title: Standardize configuration approaches
description: When documenting or implementing configuration procedures, prioritize
  standard, unified approaches over custom or platform-specific solutions. This applies
  to setup scripts, environment activation, and configuration management.
repository: commaai/openpilot
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 58214
---

When documenting or implementing configuration procedures, prioritize standard, unified approaches over custom or platform-specific solutions. This applies to setup scripts, environment activation, and configuration management.

For setup procedures, favor consolidated scripts that work across platforms:
```bash
# Preferred: unified approach
tools/op.sh setup

# Avoid: platform-specific manual steps
# Ubuntu 24.04:
# tools/ubuntu_setup.sh
# macOS:
# tools/mac_setup.sh
```

For environment management, stick to familiar standard practices rather than introducing custom commands:
```bash
# Preferred: standard Python environment activation
source .env/bin/activate

# Avoid: custom commands that require special knowledge
openpilot_shell
```

This approach reduces cognitive load for developers, leverages existing knowledge, and maintains consistency across different environments. Only introduce custom configuration methods when standard approaches are insufficient for the specific use case.