---
title: Event-triggered network requests
description: When implementing user interactions that trigger network requests, use
  precise event handling techniques to ensure reliable network operations. Specifically,
  check event properties like `event.button` (which button was pressed) rather than
  `event.buttons` (which buttons are currently pressed) to correctly handle user intent.
repository: mui/material-ui
label: Networking
language: JavaScript
comments_count: 4
repository_stars: 96063
---

When implementing user interactions that trigger network requests, use precise event handling techniques to ensure reliable network operations. Specifically, check event properties like `event.button` (which button was pressed) rather than `event.buttons` (which buttons are currently pressed) to correctly handle user intent.

For mouse events that initiate network calls:
```javascript
// Only handle network request when the main button is pressed (left click)
const handleRequestButtonClick = (event) => {
  if (event.button === 0) {  // 0 represents left mouse button
    fetchDataFromAPI();
  }
};
```

For keyboard events, use appropriate event management to prevent unintended network activity:
```javascript
const handleKeyDown = (event) => {
  // Prevent navigation shortcuts from triggering network requests
  if (event.altKey && (event.key === 'ArrowLeft' || event.key === 'ArrowRight')) {
    event.stopPropagation();
    return;
  }
  
  // Proceed with network request if Enter key is pressed
  if (event.key === 'Enter') {
    fetchDataFromAPI();
  }
};
```

This prevents accidental network requests from middle/right clicks or keyboard shortcuts, improving user experience and reducing unnecessary server load.