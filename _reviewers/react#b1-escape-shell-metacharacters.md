---
title: Escape shell metacharacters
description: 'When writing CI/workflow shell commands (or any bash/sh `run` block),
  treat message text as data: escape shell metacharacters—especially backticks—so
  they cannot be interpreted as command substitution.'
repository: facebook/react#b1
label: Security
language: Yaml
comments_count: 1
repository_stars: 251878
---

When writing CI/workflow shell commands (or any bash/sh `run` block), treat message text as data: escape shell metacharacters—especially backticks—so they cannot be interpreted as command substitution.

Example (safe):
```bash
git diff --exit-code || (
  echo "There was a change to the Fizz runtime. Run \`yarn generate-inline-fizz-runtime\` and check in the result." 
  && false
)
```

Avoid patterns like:
```bash
echo "... Run `yarn generate-inline-fizz-runtime` ..."  # may execute the command
```

Apply this anywhere you embed user-facing “run this command” text inside shell-evaluated strings, including error messages and logging.