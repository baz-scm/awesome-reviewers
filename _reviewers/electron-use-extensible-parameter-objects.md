---
title: Use extensible parameter objects
description: When designing APIs that may need additional parameters in the future,
  use objects instead of individual parameters to enable extension without breaking
  changes. This approach allows new properties to be added while maintaining backward
  compatibility.
repository: electron/electron
label: API
language: Markdown
comments_count: 12
repository_stars: 117644
---

When designing APIs that may need additional parameters in the future, use objects instead of individual parameters to enable extension without breaking changes. This approach allows new properties to be added while maintaining backward compatibility.

Instead of adding individual parameters that create rigid function signatures:

```js
// Avoid: Hard to extend without breaking changes
win.setVibrancy(type, animate, animationDuration)
```

Use an options object that can accommodate future parameters:

```js
// Preferred: Extensible design
win.setVibrancy(type, {
  animate: boolean,
  animationDuration: number
  // Future properties can be added here
})
```

For events, group related parameters into a details object rather than individual parameters:

```js
// Avoid: Individual parameters
app.on('notification-activation', (event, appUserModelId, invokedArgs, dataCount, inputData) => {})

// Preferred: Details object
app.on('notification-activation', (event, details) => {
  // details.appUserModelId, details.invokedArgs, etc.
})
```

This pattern is especially important for APIs that interact with evolving web standards or platform capabilities, where new options frequently become available. Consider how Chrome extension APIs and DOM APIs use this pattern successfully - they can add new properties without breaking existing code that only uses a subset of the available options.