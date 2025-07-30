---
title: Environment variable patterns
description: Use consistent patterns for environment variable handling in shell scripts.
  Always provide sensible defaults using the `${VAR:-default}` syntax, validate required
  variables early with clear error messages, and preserve the ability to override
  configuration values.
repository: Unstructured-IO/unstructured
label: Configurations
language: Shell
comments_count: 5
repository_stars: 12117
---

Use consistent patterns for environment variable handling in shell scripts. Always provide sensible defaults using the `${VAR:-default}` syntax, validate required variables early with clear error messages, and preserve the ability to override configuration values.

For variables with defaults:
```bash
strategies=${STRATEGIES:=fast,hi_res,ocr_only}
RUN_SCRIPT=${RUN_SCRIPT:-unstructured-ingest}
PYTHONPATH=${PYTHONPATH:-.}
```

For required variables, validate early and provide helpful error messages:
```bash
if [ -z "$VECTARA_OAUTH_CLIENT_ID" ]; then
  echo "Skipping VECTARA ingest test because VECTARA_OAUTH_CLIENT_ID env var is not set."
  exit 0
fi
```

Document configurable environment variables in script comments or usage instructions to make them discoverable for users who aren't familiar with shell scripting. This approach allows scripts to work out-of-the-box with reasonable defaults while remaining flexible for different environments and use cases.