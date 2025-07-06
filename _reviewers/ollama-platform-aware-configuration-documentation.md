---
title: Platform-aware configuration documentation
description: Always document platform-specific configuration differences and requirements
  thoroughly. When writing documentation or implementing configuration-related code,
  explicitly address variations across different operating systems and environments.
repository: ollama/ollama
label: Configurations
language: Markdown
comments_count: 4
repository_stars: 145705
---

Always document platform-specific configuration differences and requirements thoroughly. When writing documentation or implementing configuration-related code, explicitly address variations across different operating systems and environments.

Key practices:
1. Specify environment variable differences by platform (e.g., temp directories use TMPDIR on Linux, but TMP/TEMP on Windows)
2. Document installation and configuration paths that may vary between systems
3. Provide appropriate command syntax for each platform, noting differences in flags or parameters
4. Include platform-specific prerequisites and setup requirements

Example:

```shell
# For temporary directory configuration:
# On Linux/macOS:
export TMPDIR=/path/with/sufficient/space

# On Windows:
set TMP=D:\path\with\sufficient\space

# When removing configuration directories:
# On Linux/macOS:
sudo rm -rf /etc/ollama  # Use -r flag for directories

# For cross-platform command examples:
ollama completion [bash|zsh|fish] > /path/to/completion/file  # Standard syntax pattern
```

Following these practices ensures configurations work correctly across different environments and helps users avoid platform-specific issues.