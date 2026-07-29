---
title: Config.yaml First Policy
description: Behavioral configuration must be owned by `config.yaml` (and documented),
  while environment variables must be limited to secrets or internal backward-compatibility
  bridges. Also ensure any filesystem default paths are profile-safe via `get_hermes_home()`.
repository: nousresearch/hermes-agent
label: Configurations
language: Python
comments_count: 6
repository_stars: 221948
---

Behavioral configuration must be owned by `config.yaml` (and documented), while environment variables must be limited to secrets or internal backward-compatibility bridges. Also ensure any filesystem default paths are profile-safe via `get_hermes_home()`.

Apply this standard:
1) **Behavioral knobs → `config.yaml`**
   - If a setting changes runtime behavior (timeouts, feature toggles, thresholds, permissions modes, debug/status behavior, etc.), add it to the relevant `config.yaml` section (with defaults in `DEFAULT_CONFIG`) and update docs/tests.
   - Prefer existing config bridges (e.g., `agent.*`, `stt.*`, `platforms.*.extra`) over new `HERMES_*` behavioral env vars.

2) **Env vars are allowed only for:
   - Secrets (e.g., API keys/tokens) and credential loading.
   - Internal compatibility**: a narrow env override that is explicitly labeled “bridge/compat” and not the primary user-facing interface.

3) **Profile-safe defaults**
   - Any default file path (logs, audit outputs, caches, state) must derive from the active profile’s home (`get_hermes_home()/...`), not `$HOME/.hermes` or hardcoded POSIX paths.

Code sketch (config-first + profile-safe default + env only as compat):

```python
import os
from pathlib import Path
from hermes_constants import get_hermes_home

_TRUEY = {"1","true","on","yes"}

def _truthy(v: str) -> bool:
    return v.strip().lower() in _TRUEY

def enabled() -> bool:
    # Internal compat bridge (optional): env overrides should not be the primary surface.
    env = os.environ.get("HERMES_SOME_FEATURE", "").strip().lower()
    if env:
        return _truthy(env)

    # Primary: config.yaml (load once via existing config helpers)
    from hermes_cli.config import load_config
    cfg = load_config() or {}
    return _truthy(str((cfg.get("agent", {}) or {}).get("some_feature", {}).get("enabled", False)))

def sink_path() -> str:
    # Profile-safe default
    default = get_hermes_home() / "logs" / "feature.log"

    # Optional compat env override for service managers
    override = os.environ.get("HERMES_SOME_FEATURE_FILE", "").strip()
    return str(Path(override).expanduser()) if override else str(default)
```

If you’re about to introduce a new `HERMES_*` env var for behavior, stop and ask: “Is this truly a secret or only internal compat?” If it’s user-facing, route it through `config.yaml` instead.