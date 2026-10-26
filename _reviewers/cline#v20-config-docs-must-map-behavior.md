---
title: Config Docs Must Map Behavior
description: 'Configuration-related documentation and examples must be deterministic,
  platform-safe, and complete about how settings affect runtime behavior.


  Apply this standard by:'
repository: cline/cline#v20
label: Configurations
language: Other
comments_count: 3
repository_stars: 70886
---

Configuration-related documentation and examples must be deterministic, platform-safe, and complete about how settings affect runtime behavior.

Apply this standard by:
- **Map every relevant config key to actual behavior**: if multiple implementations/bundles exist, document the override key and the resulting mode (and what the default/auto does).
- **Make path handling OS-correct**: don’t assume `~` (or other expansions) is universally understood; if a path is important to users, either spell out the platform-safe equivalent or clearly explain the expansion behavior.
- **Handle config-generated artifacts safely across workspace layouts**: when config writes caches/secrets into the workspace, ensure `.gitignore` patterns actually cover nested cases (use recursive patterns when needed) so keys aren’t accidentally committed.

Example patterns to follow:
```text
# Deterministic feature-flag override
# (VS Code example)
cline.rollout.bundleOverride = "next" | "legacy"  # choose implementation explicitly
# "auto" follows the rollout.

# Safe ignores for config-managed cached settings
**/.cline/enterprise/
**/.cline/remote-config/
```

If you can’t confidently state how a setting behaves on each supported platform/product (including different builds), treat it as a documentation bug and fix the source of truth (code + docs), not just the wording.