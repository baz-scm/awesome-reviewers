---
title: consistent dependency formatting
description: Maintain consistent formatting and organization when managing dependencies
  in package.json files. Use semver range notation (^) consistently for all dependencies
  to allow compatible updates, and make targeted changes rather than bulk updates
  to preserve clean git history and blame information.
repository: ant-design/ant-design
label: Code Style
language: Json
comments_count: 2
repository_stars: 95882
---

Maintain consistent formatting and organization when managing dependencies in package.json files. Use semver range notation (^) consistently for all dependencies to allow compatible updates, and make targeted changes rather than bulk updates to preserve clean git history and blame information.

Example:
```json
// Good - consistent semver ranges and targeted updates
"@biomejs/biome": "^1.0.0",
"@babel/runtime": "^7.27.0"

// Avoid - missing semver range and bulk updates
"@biomejs/biome": "1.0.0"  // Missing ^ prefix
```

When updating dependencies, only modify the specific packages you intend to upgrade rather than running broad update commands that change multiple unrelated dependencies simultaneously.