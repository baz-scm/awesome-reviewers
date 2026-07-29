---
title: Single Source Config
description: 'Ensure workflow configuration (env vars, inputs, config lists) has a
  single authoritative definition and a clearly documented consumer.


  Apply this when editing GitHub Actions/workflow configs or config-driven automation:'
repository: QwenLM/qwen-code
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 26407
---

Ensure workflow configuration (env vars, inputs, config lists) has a single authoritative definition and a clearly documented consumer.

Apply this when editing GitHub Actions/workflow configs or config-driven automation:
- **No dead config:** If a variable is declared but never read by any step/script, remove it or comment the intended future consumer.
- **No shadowing:** Don’t define the same setting at multiple levels (e.g., job `env:` and step `env:`) unless the override is intentional and documented. Prefer keeping the setting only where it’s consumed.
- **No duplicated literals:** Don’t hardcode the same list/constant in multiple places (workflow + router script + other steps). Derive it from one source (script output or a single config file) and pass it through outputs.

Example (pattern): derive the maintainer list once and reuse it, instead of duplicating:
```yaml
- name: Classify
  id: classify
  run: |
    # router outputs JSON including full maintainer list
    result="$(node router.mjs ... )"
    echo "maintainers=$(echo "$result" | jq -c '.maintainers')" >> "$GITHUB_OUTPUT"

- name: Apply review requests
  env:
    MAINTAINERS: '${{ steps.classify.outputs.maintainers }}'
  run: |
    # use MAINTAINERS as the single source of truth
    node apply.mjs --maintainers "$MAINTAINERS"
```
This prevents drift, makes changes predictable, and avoids confusing behavior caused by precedence/overrides or unused settings.