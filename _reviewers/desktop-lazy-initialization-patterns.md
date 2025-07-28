---
title: Lazy initialization patterns
description: Avoid repeatedly performing expensive operations like adding event handlers,
  loading resources, or fetching preferences. Instead, initialize these resources
  once when first needed and reuse them thereafter. This prevents memory leaks, reduces
  unnecessary work, and improves performance.
repository: zen-browser/desktop
label: Performance Optimization
language: Other
comments_count: 3
repository_stars: 34711
---

Avoid repeatedly performing expensive operations like adding event handlers, loading resources, or fetching preferences. Instead, initialize these resources once when first needed and reuse them thereafter. This prevents memory leaks, reduces unnecessary work, and improves performance.

Key principles:
- Initialize event handlers during component setup, not in frequently-called methods
- Load scripts and resources on-demand rather than eagerly
- Cache preference values using lazy observers instead of fetching repeatedly

Example of problematic code:
```javascript
openTabsPopup(event) {
  // BAD: Adds new event handler every time popup opens
  search.addEventListener('input', () => {
    // handler logic
  });
  
  // BAD: Fetches preference on every call
  if(Services.prefs.getBoolPref("zen.some-pref", false)) {
    // logic
  }
}
```

Better approach:
```javascript
constructor() {
  // Initialize event handlers once during setup
  this.#setupEventHandlers();
  // Setup lazy preference observer
  this.#setupPrefObserver();
}

loadResourcesOnDemand() {
  if (!this.#resourcesLoaded) {
    Services.scriptloader.loadSubScript("chrome://browser/content/resource.mjs", this);
    this.#resourcesLoaded = true;
  }
}
```