---
title: Safe configuration defaults
description: 'When writing run/config scripts, prefer *local, opt-in* environment
  changes and *guarded* defaults.


  **Rules**

  1. **Don’t mutate persistent user config** (e.g., appending to `~/.bashrc`/`~/.profile`).
  If you need PATH changes, set them for the current process only (e.g., `export PATH=...`
  inside the script).'
repository: karpathy/nanochat
label: Configurations
language: Shell
comments_count: 3
repository_stars: 53189
---

When writing run/config scripts, prefer *local, opt-in* environment changes and *guarded* defaults.

**Rules**
1. **Don’t mutate persistent user config** (e.g., appending to `~/.bashrc`/`~/.profile`). If you need PATH changes, set them for the current process only (e.g., `export PATH=...` inside the script).
2. **Avoid forcing hardware/stack overrides by default.** Hardware-specific env vars (like ROCm/GFX overrides) should be enabled only when explicitly requested or when you can confidently detect the target GPU.
3. **Install system dependencies only when required, and only after detection.** If a dependency is needed (e.g., headers for compilation), detect its presence and install conditionally; keep messaging clear so it’s obvious why the install happened.

**Example pattern**
```bash
#!/usr/bin/env bash
set -euo pipefail

# Local PATH change (no ~/.bashrc mutation)
if command -v uv &>/dev/null; then :; else
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"

# Conditional system dependency (only if missing)
if ! dpkg -s python3-dev &>/dev/null; then
  echo "Installing python3-dev (needed for Python.h during compilation)"
  sudo apt-get update && sudo apt-get install -y python3-dev
fi

# Hardware override: opt-in via env var
# e.g. export HSA_OVERRIDE_GFX_VERSION=11.0.0 before running if needed
: "${HSA_OVERRIDE_GFX_VERSION:=}"
if [ -n "${HSA_OVERRIDE_GFX_VERSION}" ]; then
  export HSA_OVERRIDE_GFX_VERSION
fi

exec python3 -m your_program "$@"
```

Applying this standard reduces cross-environment breakage (VM/container/bare metal), prevents unintended side effects on developers’ shells, and avoids configuration values that can harm unsupported hardware.