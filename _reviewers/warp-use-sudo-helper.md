---
title: Use Sudo Helper
description: When writing shell scripts that run privileged operations, never call
  `sudo` directly or execute such commands silently. Centralize privilege escalation
  in a helper that (1) prints the exact command being run, (2) prompts for confirmation
  by default, and (3) provides an explicit, documented non-interactive escape hatch
  for CI (e.g., an env var like...
repository: warpdotdev/warp
label: Security
language: Other
comments_count: 1
repository_stars: 56893
---

When writing shell scripts that run privileged operations, never call `sudo` directly or execute such commands silently. Centralize privilege escalation in a helper that (1) prints the exact command being run, (2) prompts for confirmation by default, and (3) provides an explicit, documented non-interactive escape hatch for CI (e.g., an env var like `WARP_BOOTSTRAP_YES=1` or auto-skip when stdin isn’t a TTY).

Example (bash):
```bash
#!/usr/bin/env bash
set -euo pipefail

warp_sudo() {
  local cmd=("$@")
  echo "About to run as sudo: ${cmd[*]}"

  if [[ "${WARP_BOOTSTRAP_YES:-false}" == "true" ]] || [[ ! -t 0 ]]; then
    sudo "${cmd[@]}"
    return
  fi

  read -r -p "Proceed? [y/N] " ans
  case "${ans}" in
    y|Y) sudo "${cmd[@]}" ;;
    *) echo "Aborted."; return 1 ;;
  esac
}

# Use the helper instead of direct sudo:
# warp_sudo brew install jq
# warp_sudo apt-get update
```

Apply this standard anywhere your scripts install system-wide packages, modify system configuration, or otherwise require super-user privileges.