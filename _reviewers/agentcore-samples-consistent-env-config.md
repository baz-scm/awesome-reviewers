---
title: Consistent env config
description: 'For scripts and tests, load configuration consistently and safely, and
  make any expensive/external prerequisite behavior opt-in.


  Apply these rules:

  1) Source the same env file(s) across related scripts (deploy/destroy/test) with
  a guarded “missing file” behavior.'
repository: awslabs/agentcore-samples
label: Configurations
language: Shell
comments_count: 3
repository_stars: 3244
---

For scripts and tests, load configuration consistently and safely, and make any expensive/external prerequisite behavior opt-in.

Apply these rules:
1) Source the same env file(s) across related scripts (deploy/destroy/test) with a guarded “missing file” behavior.
2) Parse env files literally as KEY=VALUE pairs and export them (avoid shell-redirection hazards from placeholder-like values).
3) Gate integration/E2E work behind explicit environment variables that default to disabled.
4) When configuration is environment-specific (e.g., AWS region differences), branch accordingly so required parameters are correct for that environment.

Example (bash pattern):
```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SAMPLE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="${ENV_FILE:-$SAMPLE_ROOT/.env}"

# Guarded env loading
if [[ -f "$ENV_FILE" ]]; then
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" || "$line" == \#* || "$line" != *=* ]] && continue
    export "${line%%=*}=${line#*=}"
  done < "$ENV_FILE"
fi

# Opt-in prerequisite gate (default OFF)
if [[ "${RUN_AWS_X402_E2E:-0}" != "1" ]]; then
  echo "Skipping E2E; set RUN_AWS_X402_E2E=1 to enable."
  exit 0
fi
```

For region-specific AWS calls, ensure the correct parameters are provided for that region (e.g., handling us-east-1 location-constraint behavior).