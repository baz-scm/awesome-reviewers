---
title: Export environment variables once
description: When writing shell scripts, set and export all environment variables
  at the top of the script rather than modifying them repeatedly throughout the script.
  This improves readability, maintainability, and prevents inconsistent environments
  between commands.
repository: nodejs/node
label: Configurations
language: Shell
comments_count: 3
repository_stars: 112178
---

When writing shell scripts, set and export all environment variables at the top of the script rather than modifying them repeatedly throughout the script. This improves readability, maintainability, and prevents inconsistent environments between commands.

For tools like Node.js or npm, prefer using local installations over globally installed versions by explicitly setting paths to include local tool directories:

```sh
# Instead of:
NODEPATH="$(../$NODE -p 'require("path").resolve("..")')"
PATH="$NODEPATH:$PATH" ../$NODE cli.js install --ignore-scripts
PATH="$NODEPATH:$PATH" ../$NODE test/run.js

# Do this:
NODEPATH="$(../$NODE -p 'require("path").resolve("..")')"
export PATH="$NODEPATH:$PATH"
../$NODE cli.js install --ignore-scripts
../$NODE test/run.js

# Or even better, if appropriate:
export PATH="$(../$NODE -p 'require("path").resolve("..")'):$PATH"
../$NODE cli.js install --ignore-scripts
../$NODE test/run.js
```

This approach ensures consistent access to required tools across the entire script and makes changes easier to implement when needed.