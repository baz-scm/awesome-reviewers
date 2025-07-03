---
title: Feature over browser detection
description: When implementing networking features that may have varying browser support,
  always use feature detection rather than user agent sniffing. Feature detection
  tests for the actual capabilities of the browser, making your code more resilient
  to browser updates and reducing maintenance burden.
repository: facebook/react
label: Networking
language: Javascript
comments_count: 2
repository_stars: 236925
---

When implementing networking features that may have varying browser support, always use feature detection rather than user agent sniffing. Feature detection tests for the actual capabilities of the browser, making your code more resilient to browser updates and reducing maintenance burden.

For example, instead of:

```javascript
const ua = navigator.userAgent;
const supportsScrollTimeline =
  typeof ScrollTimeline === 'function' &&
  (ua.indexOf('Safari') === -1 ||
    (ua.indexOf('iPhone') === -1 && ua.indexOf('iPad') === -1));
```

Prefer a capability-based approach:

```javascript
// Check if the feature itself works correctly
function isScrollTimelineSupported() {
  try {
    // Test actual functionality instead of browser identification
    const timeline = new ScrollTimeline();
    // Additional runtime verification if needed
    return true;
  } catch (e) {
    return false;
  }
}

const supportsScrollTimeline = isScrollTimelineSupported();
```

For modern network APIs like WebSocketStream that lack universal support, implement feature detection with graceful fallbacks rather than maintaining browser-specific code paths. This approach creates more maintainable networking code that adapts to evolving browser implementations without requiring constant updates to browser detection logic.