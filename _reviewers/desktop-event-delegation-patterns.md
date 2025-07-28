---
title: event delegation patterns
description: When handling events in web applications, especially those involving
  network-triggered UI updates or real-time data streams, prefer event delegation
  over individual element listeners for better performance and maintainability. Use
  container-level event listeners and check the event target rather than attaching
  listeners to each individual element.
repository: zen-browser/desktop
label: Networking
language: Other
comments_count: 2
repository_stars: 34711
---

When handling events in web applications, especially those involving network-triggered UI updates or real-time data streams, prefer event delegation over individual element listeners for better performance and maintainability. Use container-level event listeners and check the event target rather than attaching listeners to each individual element.

This approach is particularly important when dealing with dynamic content that may be updated based on network responses, websocket messages, or API calls, as it ensures event handlers remain functional even when DOM elements are added or removed dynamically.

Example:
```javascript
// Preferred: Event delegation
gBrowser.tabContainer.addEventListener('dblclick', (event) => {
  if (event.target.matches('.tab-label')) {
    // Handle the event
  }
});

// Avoid: Individual listeners on each element
tabs.forEach(tab => {
  tab.addEventListener('dblclick', handler);
});
```

This pattern reduces memory overhead and ensures consistent behavior when UI elements are dynamically updated from network data sources.