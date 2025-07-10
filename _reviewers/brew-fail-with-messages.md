---
title: Fail with messages
description: Functions and scripts should never fail silently. When detecting error
  conditions, always provide clear error messages to stderr that include context about
  what failed and why, then return an appropriate non-zero exit code. For user-facing
  commands, include guidance about correct usage when applicable.
repository: Homebrew/brew
label: Error Handling
language: Shell
comments_count: 3
repository_stars: 44168
---

Functions and scripts should never fail silently. When detecting error conditions, always provide clear error messages to stderr that include context about what failed and why, then return an appropriate non-zero exit code. For user-facing commands, include guidance about correct usage when applicable.

Example:
```bash
url_get() {
  if [[ ${#} -eq 0 ]]; then
    echo "Error: url_get requires at least one argument (URL)" >&2
    return 1
  fi
  
  # Function implementation...
}

# Usage with error checking
eval RESULTS=( $(url_get "${URL}" param1 param2) )
if [[ ${#RESULTS[@]} -ne 2 ]]; then
  echo "Error: Failed to parse URL=${URL}!" >&2
  exit 1
fi
```