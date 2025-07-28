---
title: cache invalidation strategy
description: Implement comprehensive cache invalidation mechanisms that automatically
  handle format changes between versions while providing clear manual removal options.
  When cache formats change, automatically detect and remove incompatible cache files
  to prevent runtime errors. Additionally, document cache locations and provide accurate
  removal commands for manual...
repository: prettier/prettier
label: Caching
language: Markdown
comments_count: 2
repository_stars: 50772
---

Implement comprehensive cache invalidation mechanisms that automatically handle format changes between versions while providing clear manual removal options. When cache formats change, automatically detect and remove incompatible cache files to prevent runtime errors. Additionally, document cache locations and provide accurate removal commands for manual cache management.

For automatic invalidation, check cache format compatibility on startup:
```bash
# Cache format changed in version 3.5, remove old cache to prevent crashes
if (cacheFormatVersion !== currentVersion) {
  removeOutdatedCache();
}
```

For manual removal, provide precise documentation with correct command syntax:
```bash
# Remove cache manually (note: no -f flag to show errors if file not found)
rm ./node_modules/.cache/prettier/.prettier-cache
```

This approach prevents crashes from incompatible cache formats while giving users clear guidance for manual cache management when needed.