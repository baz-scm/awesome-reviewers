---
title: Self-documenting code naming
description: Method, parameter, and variable names should clearly describe their purpose
  and behavior, making code self-documenting. Choose names that indicate exactly what
  the code does and how it behaves with different inputs.
repository: maplibre/maplibre-native
label: Naming Conventions
language: Other
comments_count: 5
repository_stars: 1411
---

Method, parameter, and variable names should clearly describe their purpose and behavior, making code self-documenting. Choose names that indicate exactly what the code does and how it behaves with different inputs.

For methods:
- Use action verbs that precisely describe the method's behavior
- Prefer `setTileCacheEnabled(bool)` over `enableTileCache(bool)` when a method can both enable and disable functionality
- Name methods like `removeDrawablesIf` rather than `observeDrawablesRemove` to clearly communicate intent

For parameters:
- Use descriptive nouns that indicate what the parameter represents
- Prefer meaningful types over boolean flags when possible (e.g., pass `center` coordinate instead of `shouldCenter: YES`)
- Follow platform conventions (e.g., use `CoordinateBounds` instead of `LatLngBounds` in iOS)

For constants and variables:
- Replace magic numbers with named constants, especially for special values:

```cpp
// Instead of this:
if (fo == 0.0) {
    return {
        .position = float4(-2.0, -2.0, -2.0, 1.0),
        
// Prefer this:
const float4 CULLED_POSITION = float4(-2.0, -2.0, -2.0, 1.0);
if (fo == 0.0) {
    return {
        .position = CULLED_POSITION,
```

Clear, descriptive naming reduces the need for comments and documentation while making code more maintainable and understandable for all developers.