---
title: Explicit Config Examples
description: 'When documentation or code behavior depends on configuration and environment
  (OS paths, shell expansions, rollout/build selection), make it explicit:

  '
repository: cline/cline#v10
label: Configurations
language: Other
comments_count: 2
repository_stars: 70869
---

When documentation or code behavior depends on configuration and environment (OS paths, shell expansions, rollout/build selection), make it explicit:

- Show OS-specific path examples (or clearly explain equivalences) instead of relying on ambiguous shorthand like `~`.
  - Example: if instructing users to use `~/.cline/plugins/`, also provide the Windows equivalent `%USERPROFILE%\.cline\plugins\` (or the correct roaming/local profile path if applicable).
- For features that vary by bundled builds/rollout, document the exact configuration key/value that controls which behavior is active, and mention any required reload.
  - Example pattern:
    ```json
    // VS Code settings.json
    {
      "cline.rollout.bundleOverride": "next"  // or "legacy"; "auto" follows rollout
    }
    ```
- Avoid “implicit correctness”: if nightly/alternate releases use different naming or keys, ensure the documented settings match the actual key derivation so the override reliably selects the intended behavior.