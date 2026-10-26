---
title: Document config semantics
description: When writing or updating configuration-related docs, explicitly document
  the *environment-specific* and *variant-specific* semantics so users can apply settings
  without guessing (especially across Windows vs Unix and across stable vs nightly/rollout
  builds).
repository: cline/cline#v24
label: Configurations
language: Other
comments_count: 2
repository_stars: 70891
---

When writing or updating configuration-related docs, explicitly document the *environment-specific* and *variant-specific* semantics so users can apply settings without guessing (especially across Windows vs Unix and across stable vs nightly/rollout builds).

Apply this checklist:
- Paths: Don’t assume users know what `~` means. Provide OS-accurate examples (or explicitly state the exact expansion target for Windows).
- Build/channel keys: If config keys differ by distribution/manifest identity (e.g., nightly vs stable), name the correct key and explain how explicit overrides select behavior; don’t rely on “it probably works.”

Example (path + override style):
```md
Global plugins: ~/.cline/plugins/
Windows example: %USERPROFILE%\\.cline\\plugins\\
Additional plugins: ~/Documents/Cline/Plugins/ (Windows: %USERPROFILE%\\Documents\\Cline\\Plugins/)

To force a specific bundle:
- Set `cline.rollout.bundleOverride` to `next` or `legacy`, then reload.
- Use `auto` to follow the rollout.
```

Keep the doc statements aligned with the implementation logic (e.g., key derivation/prefix rules and which build a given override targets).