---
title: Feature detection over sniffing
description: When working with browser-specific networking APIs or features, always
  use feature detection instead of user agent sniffing. Feature detection tests for
  the actual functionality rather than attempting to identify the browser, resulting
  in more reliable code that's easier to maintain and less prone to breaking when
  browsers change.
repository: facebook/react
label: Networking
language: Javascript
comments_count: 2
repository_stars: 236926
---

When working with browser-specific networking APIs or features, always use feature detection instead of user agent sniffing. Feature detection tests for the actual functionality rather than attempting to identify the browser, resulting in more reliable code that's easier to maintain and less prone to breaking when browsers change.

Instead of:
```javascript
const ua = navigator.userAgent;
const supportsFeature =
  typeof Feature === 'function' &&
  (ua.indexOf('Safari') === -1 ||
    (ua.indexOf('iPhone') === -1 && ua.indexOf('iPad') === -1));
```

Prefer:
```javascript
// Check if the API exists and works as expected
const supportsFeature = typeof Feature === 'function' && 
  (function() {
    try {
      // Minimal test of the actual functionality
      return Feature.prototype.hasOwnProperty('requiredMethod');
    } catch (e) {
      return false;
    }
  })();

// Or for network-related features, test a small operation
function checkNetworkFeatureSupport() {
  if (typeof WebSocketStream !== 'function') return false;
  
  try {
    // Test minimal functionality
    return true;
  } catch (e) {
    return false;
  }
}
```

This approach is particularly important for networking APIs like WebSockets, Fetch, and streaming interfaces where implementation details vary significantly across browsers.