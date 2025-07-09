---
title: In-tree build configurations
description: Keep all build configuration files (Snapcraft, Flatpak manifests, etc.)
  in the repository alongside your code to ensure they are tested, versioned, and
  maintained together with the application. This approach facilitates CI testing,
  allows for regression detection, and ensures consistency across distribution methods.
repository: ghostty-org/ghostty
label: CI/CD
language: Yaml
comments_count: 4
repository_stars: 32864
---

Keep all build configuration files (Snapcraft, Flatpak manifests, etc.) in the repository alongside your code to ensure they are tested, versioned, and maintained together with the application. This approach facilitates CI testing, allows for regression detection, and ensures consistency across distribution methods.

Include multiple build variants when appropriate (e.g., release vs. development builds):

```yaml
# Example Flatpak manifest with development variant
app-id: com.example.app
runtime: org.gnome.Platform
# ... common configuration ...

# Production build
modules:
  - name: app
    buildsystem: simple
    build-commands:
      - zig build -Doptimize=ReleaseFast

# With corresponding development variant
# com.example.app.Devel.yml
app-id: com.example.app.Devel
runtime: org.gnome.Platform
# ... common configuration ...
modules:
  - name: app
    buildsystem: simple
    build-commands:
      - zig build -Doptimize=Debug
```

Configure your CI workflows to verify all distribution methods on appropriate triggers (e.g., only run on relevant branches) and optimize test matrices by eliminating redundant tests that wouldn't provide additional signal. This ensures reliable builds across all supported platforms while keeping CI/CD pipelines efficient.