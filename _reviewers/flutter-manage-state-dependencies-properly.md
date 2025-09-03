---
title: Manage state dependencies properly
description: Ensure components establish explicit dependencies when they need to react
  to external changes, and avoid state updates during build phases to prevent rendering
  conflicts.
repository: flutter/flutter
label: React
language: Other
comments_count: 2
repository_stars: 172252
---

Ensure components establish explicit dependencies when they need to react to external changes, and avoid state updates during build phases to prevent rendering conflicts.

When components depend on external state (like context or inherited data), use dependency-establishing patterns rather than direct lookups that don't trigger rebuilds:

```dart
// Problematic: Overlay.of doesn't establish dependency
final overlayState = Overlay.of(context);

// Better: Use InheritedWidget-based approach that establishes dependencies
// This ensures rebuilds when the overlay changes
```

When state changes occur during build phases (like in didChangeDependencies), defer state updates to avoid "setState during build" errors:

```dart
void handleCloseRequest() {
  if (widget.onCloseRequested != null) {
    if (SchedulerBinding.instance.schedulerPhase != SchedulerPhase.persistentCallbacks) {
      // Defer to avoid setState during build
      SchedulerBinding.instance.addPostFrameCallback((_) {
        widget.onCloseRequested!();
      });
    } else {
      widget.onCloseRequested!();
    }
  }
}
```

This prevents runtime errors and ensures predictable component behavior, similar to React's rules about not calling setState during render and properly managing effect dependencies.