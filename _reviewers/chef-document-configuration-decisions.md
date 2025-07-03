---
title: Document configuration decisions
description: Add clear comments explaining the rationale behind configuration decisions,
  especially for workarounds, compatibility fixes, or environment-specific settings.
  This helps future maintainers understand why certain configurations exist and prevents
  accidental removal of necessary settings during refactoring.
repository: chef/chef
label: Configurations
language: Yaml
comments_count: 4
repository_stars: 7860
---

Add clear comments explaining the rationale behind configuration decisions, especially for workarounds, compatibility fixes, or environment-specific settings. This helps future maintainers understand why certain configurations exist and prevents accidental removal of necessary settings during refactoring.

Good examples:
```yaml
# back compat for pre-unified-/usr distros, do not add new OSes
- remote: sudo ln -s /usr/bin/install /bin/install
```

```yaml
# We have to use 20.04 host for these operations otherwise 
# the dokken images throw timedatectl error
linux-2004-host:
```

Prefer specific version identifiers over relative terms (like "latest") to ensure reproducibility and prevent unexpected behavior when defaults change:
```yaml
# Instead of: name: macos-latest # arm64
- name: macos-14 # arm64
```
