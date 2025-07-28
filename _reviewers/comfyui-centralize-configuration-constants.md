---
title: centralize configuration constants
description: Configuration values, constants, and default settings should be defined
  in a single location and referenced from there, rather than duplicated across multiple
  files or functions. This prevents inconsistencies, reduces maintenance burden, and
  ensures that changes to configuration values only need to be made in one place.
repository: comfyanonymous/ComfyUI
label: Configurations
language: JavaScript
comments_count: 2
repository_stars: 83726
---

Configuration values, constants, and default settings should be defined in a single location and referenced from there, rather than duplicated across multiple files or functions. This prevents inconsistencies, reduces maintenance burden, and ensures that changes to configuration values only need to be made in one place.

When you find the same configuration value appearing in multiple locations, extract it to a shared constant or configuration object. For example:

```javascript
// Bad - duplicated constant
const workflow_count = 10; // in app.js
// ...and the same value hardcoded elsewhere in ui.js

// Bad - duplicated default value  
const delta = 0.025; // in one function
let delta = localStorage.getItem("...") || "0.1" // different default elsewhere

// Good - centralized configuration
const CONFIG = {
  WORKFLOW_COUNT: 10,
  EDIT_ATTENTION_DELTA: 0.1
};

// Reference the centralized value
const workflow_count = CONFIG.WORKFLOW_COUNT;
let delta = localStorage.getItem("...") || CONFIG.EDIT_ATTENTION_DELTA;
```

This approach ensures that configuration changes are atomic and reduces the risk of inconsistent behavior across your application.