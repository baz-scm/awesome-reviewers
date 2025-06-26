---
title: "Document code intent"
description: "Add clear comments that explain the intent and behavior of code that might not be immediately obvious to other developers. Meaningful comments should provide context about why the code exists and how it works."
repository: "facebook/react"
label: "Documentation"
language: "JavaScript"
comments_count: 2
repository_stars: 237000
---

Add clear comments that explain the intent and behavior of code that might not be immediately obvious to other developers. Meaningful comments should provide context about why the code exists and how it works, especially for:

1. Complex test cases:
```javascript
await waitForAll([
  'Suspend! [Hi]', 
  'Loading...', 
  
  // pre-warming
  'Suspend! [Hi]'
]);
```

2. Configuration options with special status:
```javascript
/**
 * 'recommended' is currently aliased to the legacy / rc recommended config to maintain backwards compatibility.
 * This is deprecated and in v6, it will switch to alias the flat recommended config.
 */
recommended: legacyRecommendedConfig,
```

Good comments focus on explaining the "why" behind code decisions rather than merely restating what the code does. They serve as documentation that remains valuable even as implementations change, helping future maintainers understand design intent and important constraints.