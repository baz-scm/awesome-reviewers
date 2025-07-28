---
title: organize code properly
description: Maintain clean code organization by separating concerns into appropriate
  classes and files. Extract large functions into smaller, focused methods, and avoid
  creating monolithic patches that become difficult to maintain.
repository: zen-browser/desktop
label: Code Style
language: Other
comments_count: 6
repository_stars: 34711
---

Maintain clean code organization by separating concerns into appropriate classes and files. Extract large functions into smaller, focused methods, and avoid creating monolithic patches that become difficult to maintain.

Key principles:
- **Separate functionality into dedicated classes/files**: When adding new features, create separate classes or files rather than extending existing ones with unrelated functionality
- **Extract complex logic into named functions**: Replace inline patches and large code blocks with well-named functions that can be called from the appropriate context
- **Follow established patterns**: Use existing architectural patterns like extending `ZenDOMOperatedFeature` and moving constructor logic into `init()` methods

Example of good organization:
```javascript
// Instead of adding methods directly to an existing large class
class ZenSplitViewLinkDrop {
  constructor(zenViewSplitter) {
    this.#zenViewSplitter = zenViewSplitter;
  }
  
  init() {
    // Initialize functionality
  }
}

// Instead of large patches, extract to functions
gZenCompactModeManager.flashSidebarIfAllowed(aInstant);

// Instead of inline patches, use event listeners
popupElement.addEventListener('popupshowing', this.updateContextMenu.bind(this));
```

This approach improves maintainability, reduces conflicts, and makes code easier to understand and modify.