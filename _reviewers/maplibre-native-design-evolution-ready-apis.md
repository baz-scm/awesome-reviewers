---
title: Design evolution-ready APIs
description: 'Design APIs that are both explicit in their usage and provide clear
  evolution paths. When designing APIs:


  1. Prefer structured objects with named fields over primitive collections or multiple
  parameters to improve clarity and self-documentation'
repository: maplibre/maplibre-native
label: API
language: Java
comments_count: 3
repository_stars: 1411
---

Design APIs that are both explicit in their usage and provide clear evolution paths. When designing APIs:

1. Prefer structured objects with named fields over primitive collections or multiple parameters to improve clarity and self-documentation

```java
// Avoid this:
CameraPosition getCameraForLatLngBounds(LatLngBounds bounds, int[] padding, double bearing, double pitch);

// Prefer this:
CameraPosition getCameraForLatLngBounds(LatLngBounds bounds, CameraPadding padding, double bearing, double pitch);

// Where CameraPadding is a well-defined class:
public class CameraPadding {
    public final int left;
    public final int top;
    public final int right;
    public final int bottom;
    
    // Constructor and other methods
}
```

2. When modifying existing APIs, analyze compatibility impacts (binary vs. source compatibility) and provide proper deprecation paths:

```java
/**
 * @deprecated Use {@link #onDidFinishRenderingFrame(boolean, RenderingStats)} instead.
 */
@Deprecated
void onDidFinishRenderingFrame(boolean fully, double frameEncodingTime, double frameRenderingTime);

/**
 * Called when the map has finished rendering a frame
 *
 * @param fully true if all frames have been rendered, false if partially rendered
 * @param stats rendering statistics
 */
void onDidFinishRenderingFrame(boolean fully, RenderingStats stats);
```

3. Consider using more generic interfaces for parameters when appropriate to allow for greater flexibility, but evaluate compatibility impacts before changing existing signatures.

Following these practices leads to more maintainable, self-documenting APIs that can evolve gracefully over time without causing unnecessary pain for API consumers.