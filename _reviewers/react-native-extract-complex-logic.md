---
title: extract complex logic
description: Break down complex functions and large files into smaller, focused units
  with clear responsibilities. Extract complex logic into well-named helper functions,
  split large files into focused modules, and prefer `const` over `let` for variables
  that won't be reassigned.
repository: facebook/react-native
label: Code Style
language: JavaScript
comments_count: 7
repository_stars: 123178
---

Break down complex functions and large files into smaller, focused units with clear responsibilities. Extract complex logic into well-named helper functions, split large files into focused modules, and prefer `const` over `let` for variables that won't be reassigned.

When functions become difficult to understand or do multiple things, extract the complex parts:

```javascript
// Instead of one large function doing everything
function parseRadialGradientCSSString(gradientContent) {
  // 50+ lines of parsing logic for shape, size, and position
  const firstPartTokens = firstPartStr.split(/\s+/);
  while (firstPartTokens.length > 0) {
    // complex parsing logic...
  }
}

// Extract into focused functions
function parseRadialGradientCSSString(gradientContent) {
  const position = parseRadialGradientPosition(firstPartStr);
  const shape = parseRadialGradientShape(firstPartStr);
  // cleaner, more focused logic
}
```

Similarly, prefer `const` for immutable variables to signal intent:

```javascript
// Instead of
let restPropsWithDefaults = {
  ...defaultProps
};

// Use
const restPropsWithDefaults = {
  ...defaultProps
};
```

When files grow beyond 200-300 lines or handle multiple distinct responsibilities, split them into focused modules organized by functionality (e.g., `StyleSheet/BackgroundImage/linearGradient.js`, `radialGradient.js`).