---
title: Keep build scripts portable
description: Build scripts should remain environment-agnostic and free from personal
  customizations or assumptions about end-user needs. Avoid including local-specific
  commands (like clipboard operations) and let consumers make their own decisions
  about optimizations like minification.
repository: browserbase/stagehand
label: CI/CD
language: Json
comments_count: 2
repository_stars: 16443
---

Build scripts should remain environment-agnostic and free from personal customizations or assumptions about end-user needs. Avoid including local-specific commands (like clipboard operations) and let consumers make their own decisions about optimizations like minification.

Personal commands like `&& cat ./lib/dom/bundle.js | pbcopy` should be removed as they're platform-specific and will fail in CI environments or on different operating systems. Similarly, avoid aggressive optimizations like minification in library builds - distributed code should remain readable and debuggable, allowing end users to apply their own build optimizations if needed.

Example of problematic build script:
```json
"bundle-dom-scripts": "esbuild ./lib/dom/index.ts --bundle --outfile=./lib/dom/bundle.js --platform=browser --target=es2015 --minify && cat ./lib/dom/bundle.js | pbcopy"
```

Better approach:
```json
"bundle-dom-scripts": "esbuild ./lib/dom/index.ts --bundle --outfile=./lib/dom/bundle.js --platform=browser --target=es2015"
```

This ensures builds work consistently across all environments and maintains code readability for debugging purposes.