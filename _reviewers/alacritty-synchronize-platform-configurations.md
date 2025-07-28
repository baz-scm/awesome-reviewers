---
title: synchronize platform configurations
description: When making configuration changes that affect multiple platform-specific
  files, ensure all related configuration files are updated consistently and test
  the changes on each target platform.
repository: alacritty/alacritty
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 59675
---

When making configuration changes that affect multiple platform-specific files, ensure all related configuration files are updated consistently and test the changes on each target platform.

Configuration changes often need to be replicated across platform-specific variants (e.g., `alacritty.yml` and `alacritty_macos.yml`). Failing to synchronize these files can lead to inconsistent behavior across platforms and user confusion.

Always identify and update all related configuration files when making changes. Additionally, verify that configuration changes work as expected on each target platform, as platform-specific behaviors can differ even with identical configuration syntax.

Example:
```yaml
# alacritty.yml
key_bindings:
  - { key: Equals,   mods: Control, action: IncreaseFontSize }
  - { key: Subtract, mods: Control, action: DecreaseFontSize }

# alacritty_macos.yml (must be updated consistently)
key_bindings:
  - { key: Equals,   mods: Command, action: IncreaseFontSize }
  - { key: Subtract, mods: Command, action: DecreaseFontSize }
```

Test configuration changes on the actual target platforms rather than assuming cross-platform compatibility, as modifier keys and system behaviors can vary between operating systems.