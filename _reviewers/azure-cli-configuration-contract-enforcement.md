---
title: Configuration Contract Enforcement
description: 'When behavior depends on configuration (files/flags/subscriptions),
  do three things: (1) derive values from the active runtime context (including any
  overrides), (2) gate feature behavior on validated completeness of required config
  inputs, and (3) eliminate hidden defaults/implicit selections.'
repository: Azure/azure-cli
label: Configurations
language: Python
comments_count: 4
repository_stars: 4592
---

When behavior depends on configuration (files/flags/subscriptions), do three things: (1) derive values from the active runtime context (including any overrides), (2) gate feature behavior on validated completeness of required config inputs, and (3) eliminate hidden defaults/implicit selections.

Apply as follows:
- Config paths/files: never build config locations from global constants if `config_dir` can be overridden. Use the resolved runtime `config_dir` from the CLI context.
- Feature flags / multi-flag options: if enabling a mode requires multiple inputs (e.g., a “BYO trio”), only set `enabled=true` when *all* required inputs are present and validation has been run; reject/avoid partial configurations.
- Explicit configuration: when creating clients/resources, pass required scoping explicitly (e.g., subscription id) rather than relying on implicit/default selection.
- Avoid brittle CLI side effects: only remove/override defaults that the CLI itself synthesized; preserve user-provided configuration.

Example pattern (flag gating):
```python
# after validate_byo_trio completeness
system_node_subnet_id = ctx.get_system_node_subnet_id()
node_subnet_id = ctx.get_node_subnet_id()

enable_mode = ctx.get_enable_hosted_system()  # true only when full trio is present
if enable_mode:
    mc.hosted_system_profile.enabled = True
    mc.hosted_system_profile.system_node_subnet_id = system_node_subnet_id
    mc.hosted_system_profile.node_subnet_id = node_subnet_id
```