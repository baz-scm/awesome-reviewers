---
title: Limit postMessage data exposure
description: When using postMessage for inter-window communication, avoid sending
  raw event data or generic message types that could expose sensitive information.
  Instead, use specific, predefined message types and only send the minimum necessary
  data.
repository: dyad-sh/dyad
label: Security
language: JavaScript
comments_count: 1
repository_stars: 16903
---

When using postMessage for inter-window communication, avoid sending raw event data or generic message types that could expose sensitive information. Instead, use specific, predefined message types and only send the minimum necessary data.

This prevents potential information leakage and reduces the attack surface for malicious code that might intercept or manipulate cross-window messages.

Example:
```javascript
// Avoid: Sending raw event data
window.parent.postMessage({
  type: "dyad-shortcut-triggered",
  key: e.key.toLowerCase(),
  eventModifiers: {
    ctrl: e.ctrlKey,
    shift: e.shiftKey
  }
});

// Prefer: Specific message type with minimal data
window.parent.postMessage({
  type: "dyad-select-component-shortcut"
});
```