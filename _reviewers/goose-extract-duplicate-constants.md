---
title: Extract duplicate constants
description: Eliminate code duplication by extracting repeated values and components
  into well-organized constants. This applies at both the variable level (extracting
  duplicate literal values) and file level (separating reusable components).
repository: block/goose
label: Code Style
language: JavaScript
comments_count: 2
repository_stars: 19037
---

Eliminate code duplication by extracting repeated values and components into well-organized constants. This applies at both the variable level (extracting duplicate literal values) and file level (separating reusable components).

For duplicate values, extract them to named constants:
```javascript
// Instead of:
const [downloadUrls, setDownloadUrls] = useState({
  deb: "https://github.com/block/goose/releases/latest",
  rpm: "https://github.com/block/goose/releases/latest"
});

// Use:
const LATEST_RELEASE_URL = "https://github.com/block/goose/releases/latest";
const [downloadUrls, setDownloadUrls] = useState({
  deb: LATEST_RELEASE_URL,
  rpm: LATEST_RELEASE_URL
});
```

For reusable components, consider separating them into individual files rather than grouping them in a single constants file:
```
// Instead of: src/components/Constants.js (with multiple components)
// Use: src/components/DesktopProviderSetup.js
//      src/components/ModelSelectionTip.js
```

This improves maintainability, reduces the risk of inconsistencies, and makes the codebase more modular and easier to navigate.