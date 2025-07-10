---
title: Structure documentation effectively
description: 'Documentation should prioritize clear organization with a logical flow
  to help developers find information quickly. Apply these practices:


  1. Use descriptive headings and titles that directly communicate content purpose'
repository: maplibre/maplibre-native
label: Documentation
language: Markdown
comments_count: 5
repository_stars: 1411
---

Documentation should prioritize clear organization with a logical flow to help developers find information quickly. Apply these practices:

1. Use descriptive headings and titles that directly communicate content purpose
```markdown
# Ways to Configure the Map
## XML Configuration
## Programmatic Configuration
## Using MapLibreMapOptions
```

2. Focus on specialized or unique content rather than explaining widely understood concepts
```markdown
// Instead of explaining JSON basics:
## Using GeoJSON in MapLibre
This guide focuses on MapLibre-specific GeoJSON implementation details.
```

3. Include complete, explicit instructions that readers can follow without additional context
```markdown
// Instead of:
You need to have the correct Rust toolchain(s) installed.

// Write:
Install the required Rust toolchain with:
```bash
rustup install 1.68.0
rustup default 1.68.0
```

4. Ensure all substantive code examples are referenced or tested to verify they remain valid as the codebase evolves
```kotlin
// Reference to a working example in the codebase
// See: examples/MapOptionsDemo.kt
val mapOptions = MapLibreMapOptions.Builder()
    .camera(CameraPosition.Builder()
        .target(LatLng(51.50550, -0.07520))
        .zoom(10.0)
        .build())
    .build()
```