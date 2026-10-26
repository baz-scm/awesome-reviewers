---
title: Config Docs Clarity
description: When writing or updating configuration documentation, ensure it’s unambiguous
  across both (a) the user’s environment (OS/path semantics) and (b) any rollout/build
  variants that change behavior.
repository: cline/cline#v14
label: Configurations
language: Other
comments_count: 2
repository_stars: 70876
---

When writing or updating configuration documentation, ensure it’s unambiguous across both (a) the user’s environment (OS/path semantics) and (b) any rollout/build variants that change behavior.

Apply this:
- Prefer explicit, OS-correct paths over shorthand.
  - If you mention `~`, also state what it expands to on supported OSes (e.g., Windows home) or provide the equivalent Windows path form.
  - If the feature depends on user profile location, call out the relevant base directory(s) (local vs roaming) or provide the exact directory users should use.
- For feature flags/rollout-dependent behavior, document the exact setting that selects the intended variant.
  - Name the full config key (e.g., `cline.rollout.bundleOverride`) and the accepted values.
  - If nightly/stable use different key prefixes or identity mappings, mention that mapping so Nightly users can override intentionally.

Example (doc snippet style):
```md
Global plugins:
- macOS/Linux: `~/.cline/plugins/`
- Windows: `%USERPROFILE%\\.cline\\plugins\\`

Project plugins:
- `<repo>/.cline/plugins/`

To explicitly choose a feature bundle (when behavior differs):
- Set `cline.rollout.bundleOverride` to `next` or `legacy`, then reload the VS Code window.
- `auto` follows rollout.
```