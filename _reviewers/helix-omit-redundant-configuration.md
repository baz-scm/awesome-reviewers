---
title: omit redundant configuration
description: Remove configuration keys that explicitly set values identical to their
  defaults. This reduces visual clutter, minimizes maintenance overhead, and prevents
  confusion about which settings are intentionally customized versus accidentally
  duplicated.
repository: helix-editor/helix
label: Configurations
language: Toml
comments_count: 2
repository_stars: 39026
---

Remove configuration keys that explicitly set values identical to their defaults. This reduces visual clutter, minimizes maintenance overhead, and prevents confusion about which settings are intentionally customized versus accidentally duplicated.

When reviewing configuration files, identify and remove keys that match default behavior. For example:

```toml
# Before - unnecessary explicit defaults
[[language]]
name = "werk"
scope = "source.werk"
file-types = [ "werk", { glob = "Werkfile" } ]
roots = []  # Remove: [] is the default
language-id = "werk"  # Remove: matches name by default

# After - clean configuration
[[language]]
name = "werk"
scope = "source.werk"
file-types = [ "werk", { glob = "Werkfile" } ]
```

This practice helps distinguish between intentional configuration choices and default values, making the actual customizations more apparent to future maintainers.