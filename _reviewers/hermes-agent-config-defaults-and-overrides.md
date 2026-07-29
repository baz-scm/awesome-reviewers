---
title: Config Defaults And Overrides
description: When introducing or changing configuration options, treat the canonical
  config defaults and override policy as the single source of truth across runtime
  and provisioning.
repository: nousresearch/hermes-agent
label: Configurations
language: Other
comments_count: 3
repository_stars: 221948
---

When introducing or changing configuration options, treat the canonical config defaults and override policy as the single source of truth across runtime and provisioning.

Apply this standard:
1) Register every new (or newly-documented) key in the canonical `DEFAULT_CONFIG` used by the loader—do not rely on `*.example` files to define runtime behavior.
2) Verify merge semantics with regression tests:
   - Absent blocks/keys are filled from `DEFAULT_CONFIG`.
   - Explicit user values in `config.yaml` must survive the merge unchanged.
3) Keep `cli-config.yaml.example` (and any public docs/comments) synchronized with `DEFAULT_CONFIG`.
4) For any install/build/enablement logic (e.g., installing optional toolsets), consult the same final user override mechanism used at runtime (e.g., `agent.disabled_toolsets`) and “soft-skip” consistently rather than reinstalling disabled components.

Minimal pattern for (1)-(2):
```py
# hermes_cli/config.py
DEFAULT_CONFIG = {
  "agent": {
    "claude_agent_sdk": {
      "streaming": False,
      "allow_metered_key": False,
      "append_file": "",
    },
  },
}

# tests should assert:
# - deep-merge fills missing blocks/keys from DEFAULT_CONFIG
# - explicit user values in config.yaml remain unchanged
# - loader output matches canonical defaults exactly
```

For (4), ensure provisioning stages mirror runtime policy (e.g., read disabled toolsets from the existing config.yaml and skip the install step with a clear skipped reason when the toolset is disabled).