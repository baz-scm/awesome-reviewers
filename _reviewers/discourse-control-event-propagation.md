---
title: Control event propagation
description: Prevent unintended network requests and interface conflicts by properly
  controlling event propagation in interactive elements. Use `event.stopImmediatePropagation()`
  when multiple event listeners on the same element or its ancestors could trigger
  conflicting network operations.
repository: discourse/discourse
label: Networking
language: JavaScript
comments_count: 2
repository_stars: 44898
---

Prevent unintended network requests and interface conflicts by properly controlling event propagation in interactive elements. Use `event.stopImmediatePropagation()` when multiple event listeners on the same element or its ancestors could trigger conflicting network operations.

This is particularly important when:
- Form submissions or network requests could be triggered by event bubbling
- Multiple components handle the same event type and could interfere with each other
- Autocomplete or similar features need to prevent default browser behavior

Example:
```javascript
case "Enter":
case "Tab":
  event.preventDefault();
  event.stopImmediatePropagation(); // Prevents other listeners from triggering unwanted network calls
```

Consider binding events to the most appropriate element level rather than relying on event bubbling, especially for network-triggering operations like prefetching or form submissions. This reduces the risk of unintended network activity and improves code maintainability.