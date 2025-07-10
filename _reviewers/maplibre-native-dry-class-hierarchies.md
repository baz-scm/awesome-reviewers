---
title: DRY class hierarchies
description: Follow the Don't Repeat Yourself (DRY) principle when designing class
  hierarchies. Extract common functionality into base classes and avoid duplicating
  state or methods in subclasses. When extending a class, delegate to parent implementations
  rather than redefining functionality.
repository: maplibre/maplibre-native
label: Code Style
language: Java
comments_count: 3
repository_stars: 1411
---

Follow the Don't Repeat Yourself (DRY) principle when designing class hierarchies. Extract common functionality into base classes and avoid duplicating state or methods in subclasses. When extending a class, delegate to parent implementations rather than redefining functionality.

**Examples of issues to avoid:**

```java
// AVOID: Duplicating state in subclass
public class TransformAuto extends Transform {
    @Nullable
    private CameraPosition cameraPosition; // Duplicate of parent state
    
    @UiThread
    public CameraPosition getCameraPosition() {
        if (cameraPosition == null) {
            cameraPosition = invalidateCameraPosition();
        }
        return cameraPosition;
    }
}

// BETTER: Delegate to parent
public class TransformAuto extends Transform {
    // No duplicate cameraPosition variable
    
    @UiThread
    public CameraPosition getCameraPosition() {
        return super.getCameraPosition(); // Delegate to parent
    }
}
```

For similar implementations across different technologies (e.g., GL and Vulkan renderers), extract shared code into common base classes. This improves maintainability and prevents bugs from inconsistent implementations.