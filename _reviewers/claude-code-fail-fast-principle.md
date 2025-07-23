---
title: Fail fast principle
description: When writing security-sensitive shell scripts, use strict error handling
  to fail immediately on errors rather than attempting fallbacks or continuing silently.
  Always include `set -euo pipefail` to exit on errors, treat unbound variables as
  errors, and propagate pipeline failures. This prevents partial application of security
  configurations that could leave...
repository: anthropics/claude-code
label: Error Handling
language: Shell
comments_count: 2
repository_stars: 25432
---

When writing security-sensitive shell scripts, use strict error handling to fail immediately on errors rather than attempting fallbacks or continuing silently. Always include `set -euo pipefail` to exit on errors, treat unbound variables as errors, and propagate pipeline failures. This prevents partial application of security configurations that could leave systems in a vulnerable state.

```bash
#!/bin/bash
# Always use strict error handling in security scripts
set -euo pipefail  # Exit on error, undefined vars, and pipeline failures
IFS=$'\n\t'        # Stricter word splitting

# Critical security operations
iptables -F
ipset create allowed-domains hash:net

# External dependencies should fail explicitly rather than silently continuing
gh_ranges=$(curl -s https://api.github.com/meta)
if [ -z "$gh_ranges" ]; then
    echo "ERROR: Failed to fetch GitHub IP ranges"
    exit 1
fi
```

By failing fast on errors, you ensure that security configurations are either completely applied or not applied at all, avoiding inconsistent states that could create security vulnerabilities. For security-critical code, avoid fallback mechanisms like the `try_cmd` pattern that might silently continue after failures.