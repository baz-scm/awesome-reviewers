---
title: Component initialization state
description: Ensure components properly handle initialization state during their lifecycle,
  particularly when being recycled or updated. Components should explicitly track
  whether they have been initialized and force initial value setting when necessary,
  rather than relying on property comparison alone.
repository: facebook/react-native
label: React
language: Other
comments_count: 2
repository_stars: 123178
---

Ensure components properly handle initialization state during their lifecycle, particularly when being recycled or updated. Components should explicitly track whether they have been initialized and force initial value setting when necessary, rather than relying on property comparison alone.

When implementing component updates, check for initialization state before comparing old and new properties:

```objc
// Instead of just comparing properties
if (oldSwitchProps.value != newSwitchProps.value) {
  [_switchView setOn:newSwitchProps.value animated:shouldAnimate];
}

// Include initialization check
if (!_isInitialValueSet || oldSwitchProps.value != newSwitchProps.value) {
  BOOL shouldAnimate = _isInitialValueSet == YES;
  [_switchView setOn:newSwitchProps.value animated:shouldAnimate];
}
```

This pattern prevents issues where recycled components retain default values that don't match the intended initial state, and ensures proper state preservation during component updates. Always consider the component's lifecycle stage when determining whether to apply property changes.