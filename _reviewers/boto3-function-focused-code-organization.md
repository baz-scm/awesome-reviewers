---
title: Function-focused code organization
description: 'Files should contain only code related to their named purpose, with
  proper organization and formatting. When adding functionality:


  1. Place code in files that match their purpose (e.g., theme-related code belongs
  in general utilities, not in specialized modules)'
repository: boto/boto3
label: Code Style
language: JavaScript
comments_count: 2
repository_stars: 9417
---

Files should contain only code related to their named purpose, with proper organization and formatting. When adding functionality:

1. Place code in files that match their purpose (e.g., theme-related code belongs in general utilities, not in specialized modules)
2. Create dedicated, well-named functions for specific tasks
3. Follow established patterns for code organization in the project
4. Run all JavaScript changes through a formatter for readability and maintainability

Example of good organization:
```js
// In custom.js (not in specialized files like loadShortbread.js)
function loadThemeFromLocalStorage(){
  document.body.dataset.theme = localStorage.getItem("theme") || "auto";
}

function runAfterDOMLoads() {
  expandSubMenu();
  makeCodeBlocksScrollable();
  setupKeyboardFriendlyNavigation();
  // Organized functions called in appropriate place
  loadThemeFromLocalStorage();
  loadShortbread();
}
```