---
title: Quote shell substitutions
description: Always enclose command substitutions in double quotes when assigning
  to variables or using in shell scripts to prevent word splitting vulnerabilities.
  Unquoted command substitutions can lead to unexpected behavior or security vulnerabilities
  if the output contains spaces or special characters, potentially enabling command
  injection attacks.
repository: elie222/inbox-zero
label: Security
language: Yaml
comments_count: 1
repository_stars: 8267
---

Always enclose command substitutions in double quotes when assigning to variables or using in shell scripts to prevent word splitting vulnerabilities. Unquoted command substitutions can lead to unexpected behavior or security vulnerabilities if the output contains spaces or special characters, potentially enabling command injection attacks.

**Example:**
```diff
# Vulnerable - may allow word splitting if output contains spaces
- echo "STORE_PATH=$(pnpm store path --silent)" >> $GITHUB_ENV

# Secure - properly quotes the command substitution
+ echo "STORE_PATH=\"$(pnpm store path --silent)\"" >> $GITHUB_ENV
```

Use automated tools like shellcheck to identify and fix these vulnerabilities in your CI/CD workflows and shell scripts.