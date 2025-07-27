---
title: defensive shell script configuration
description: Configure shell scripts with defensive practices to ensure reliability
  and debuggability. Use appropriate `set` options for error handling and debugging,
  implement safe defaults that require explicit opt-in for risky operations, and preserve
  execution state when changing directories.
repository: snyk/cli
label: Configurations
language: Shell
comments_count: 3
repository_stars: 5178
---

Configure shell scripts with defensive practices to ensure reliability and debuggability. Use appropriate `set` options for error handling and debugging, implement safe defaults that require explicit opt-in for risky operations, and preserve execution state when changing directories.

Key practices:
- Use `set -ex` instead of just `set -e` to output commands as they execute for better debugging
- Default to safe behaviors and require explicit conditions for potentially risky operations (e.g., defaulting to dev releases and opting into stable releases only on exact matches)
- Preserve directory state using `pushd`/`popd` instead of `cd` when temporary directory changes are needed
- Document supported configuration values and their behaviors clearly

Example of defensive directory handling:
```bash
# Instead of:
cd "${PROJECT_PATH}"
pipenv install

# Use:
pushd "${PROJECT_PATH}"
pipenv install
popd
```

This approach prevents unintended side effects on subsequent script execution and makes scripts more predictable in different environments.