---
title: Ensure cross-platform compatibility
description: Write code that works consistently across different platforms and environments.
  Avoid using Unicode symbols or special characters that may not render properly in
  all terminals or logging systems, as they can cause display issues or interfere
  with automated processing. Use portable system paths and commands that work across
  different operating systems.
repository: opengrep/opengrep
label: Code Style
language: Shell
comments_count: 2
repository_stars: 1546
---

Write code that works consistently across different platforms and environments. Avoid using Unicode symbols or special characters that may not render properly in all terminals or logging systems, as they can cause display issues or interfere with automated processing. Use portable system paths and commands that work across different operating systems.

For shell scripts, use `#!/usr/bin/env bash` instead of `#!/bin/bash` to ensure the script works on systems where bash is installed in different locations. Avoid fancy Unicode symbols like ⚠️ in output messages, opting instead for plain ASCII characters that display consistently everywhere.

Example:
```bash
# Good - portable and compatible
#!/usr/bin/env bash -e
echo "WARNING: attempt failed, retrying..."

# Avoid - may not work on all systems
#!/bin/bash -e  
echo "⚠️ attempt failed, retrying..."
```

This ensures your code maintains consistent behavior and appearance regardless of the target environment, improving reliability and user experience across different systems and tools.