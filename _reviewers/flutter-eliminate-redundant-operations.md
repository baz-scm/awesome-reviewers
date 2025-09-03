---
title: Eliminate redundant operations
description: Identify and remove unnecessary operations that impact performance, including
  redundant checks, duplicate calculations, unnecessary allocations, and redundant
  code paths. This is especially critical in hot paths like widget rebuilds, message
  handling, and frequently called methods.
repository: flutter/flutter
label: Performance Optimization
language: Other
comments_count: 5
repository_stars: 172252
---

Identify and remove unnecessary operations that impact performance, including redundant checks, duplicate calculations, unnecessary allocations, and redundant code paths. This is especially critical in hot paths like widget rebuilds, message handling, and frequently called methods.

Examples of redundant operations to avoid:

1. **Redundant null/validation checks**: Remove checks that are already handled by the called function:
```dart
// Avoid - parseFloat already handles NaN
if (parsed != null && !parsed.isNaN) {
  styleProperty = parsed;
}

// Better - let parseFloat handle it
styleProperty = parsed;
```

2. **Unnecessary allocations in hot paths**: Avoid creating new objects on every call, especially in message handlers or frequent operations:
```dart
// Avoid - allocates list on every message
final List<Handler> handlers = List<Handler>.from(_messageHandlers);

// Better - use debug assertions to prevent modification during iteration
```

3. **Expensive operations during rebuilds**: Move costly operations like ancestor chain walks out of build methods:
```dart
// Avoid - walks ancestor chain every rebuild
if (Navigator.maybeOf(context, rootNavigator: true) != this) {

// Better - move to didChangeDependencies
```

4. **Duplicate calculations**: Restructure code to avoid computing the same value multiple times:
```dart
// Avoid - computes lerpValue twice
double lerpValue = ui.lerpDouble(widget.min, widget.max, value)!;
if (widget.divisions != null) {
  lerpValue = (lerpValue * widget.divisions!).round() / widget.divisions!;
}

// Better - use if-else with single computation per path
```

5. **Redundant code paths**: Remove unnecessary processing when simpler approaches achieve the same result, especially when API changes make certain fallback logic obsolete.