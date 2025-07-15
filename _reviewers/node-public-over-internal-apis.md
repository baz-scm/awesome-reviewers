---
title: Public over internal APIs
description: When designing or implementing APIs, always prefer publicly documented
  APIs over internal ones. Internal APIs may change without notice as they aren't
  subject to semantic versioning guarantees.
repository: nodejs/node
label: API
language: JavaScript
comments_count: 7
repository_stars: 112178
---

When designing or implementing APIs, always prefer publicly documented APIs over internal ones. Internal APIs may change without notice as they aren't subject to semantic versioning guarantees.

If you need functionality that's only available through internal APIs, either:

1. Look for an equivalent public API that might already exist
2. Consider creating a proper public API with appropriate documentation

For example, instead of using internal modules:

```javascript
// Avoid this
const { setSourceMapsSupport } = require('internal/source_map/source_map_cache');
const { SourceMap } = require('internal/source_map/source_map');

// Prefer this
const { setSourceMapsSupport } = require('node:module');
const { SourceMap } = require('node:module');
```

When exposing new APIs, ensure they're properly documented and don't leak internal implementation details. If an API returns values with specific formats (like 'commonjs-typescript'), either document these formats as part of the public contract or convert them to standard documented values.

Using internal APIs can lead to code that breaks unexpectedly during updates, creates maintenance burdens, and prevents APIs from being properly stabilized in the future.