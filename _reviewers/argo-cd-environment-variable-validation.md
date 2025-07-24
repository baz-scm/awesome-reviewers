---
title: Environment variable validation
description: Scripts that depend on environment variables should validate their presence
  and values early, providing clear error messages that guide users toward resolution.
  When checking environment variables, ensure logical flow doesn't create unreachable
  code blocks.
repository: argoproj/argo-cd
label: Configurations
language: Shell
comments_count: 2
repository_stars: 20149
---

Scripts that depend on environment variables should validate their presence and values early, providing clear error messages that guide users toward resolution. When checking environment variables, ensure logical flow doesn't create unreachable code blocks.

For boolean environment variables, validate the expected values and provide actionable feedback:

```bash
# Good: Clear validation with actionable error message
if [ "$ARGOCD_REDIS_LOCAL" = 'true' ]; then
    if ! command -v redis-server &>/dev/null; then
        echo "Redis server is not installed locally. Please install Redis or set ARGOCD_REDIS_LOCAL to false."
        exit 1
    fi
    # Continue with local Redis setup...
fi

# Avoid: Logic that makes subsequent code unreachable
if [ "$ARGOCD_REDIS_LOCAL" = 'true' ] && ! command -v redis-server &>/dev/null; then
    echo "Redis server not found"
    exit 1  # This prevents local Redis startup code from running
fi
```

Always structure conditional logic to ensure all valid configuration paths remain accessible and provide specific guidance on how to resolve configuration issues.