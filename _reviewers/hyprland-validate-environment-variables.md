---
title: validate environment variables
description: Always validate that environment variables are properly defined and consistently
  named before using them in scripts or build processes. Undefined or misnamed variables
  can cause silent failures or unexpected behavior in builds and deployments.
repository: hyprwm/Hyprland
label: Configurations
language: Shell
comments_count: 2
repository_stars: 28863
---

Always validate that environment variables are properly defined and consistently named before using them in scripts or build processes. Undefined or misnamed variables can cause silent failures or unexpected behavior in builds and deployments.

Check for variable existence and provide meaningful defaults or error messages. Ensure variable names are consistent across different build environments (development, CI, packaging systems like Nix).

Example of problematic code:
```bash
# Bad: Using undefined variable
MESSAGE=$(git show ${GIT_COMMIT_HASH} | head -n 5 | tail -n 1)

# Better: Use defined variable or provide default
HASH=$(git rev-parse HEAD)
MESSAGE=$(git show ${HASH:-HEAD} | head -n 5 | tail -n 1)
```

Consider using build system features like CMake's `add_compile_definitions` instead of shell script environment variable manipulation when possible, as build systems provide better validation and error handling.