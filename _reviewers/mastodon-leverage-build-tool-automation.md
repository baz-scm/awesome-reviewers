---
title: leverage build tool automation
description: Modern build tools like Vite automatically handle many performance optimizations
  that previously required manual implementation. Trust these automated capabilities
  rather than duplicating effort with manual resource hints and preloading directives.
repository: mastodon/mastodon
label: Performance Optimization
language: Other
comments_count: 2
repository_stars: 48691
---

Modern build tools like Vite automatically handle many performance optimizations that previously required manual implementation. Trust these automated capabilities rather than duplicating effort with manual resource hints and preloading directives.

Build tools automatically preload chunks that entrypoints depend on, including support for early hints when available. This eliminates the need for manual preload directives in most cases.

However, be aware of exceptions where manual intervention may still be beneficial:
- Dynamically imported scripts are not preloaded by default
- Critical resources that need explicit prioritization

Example of removing redundant manual preloading:
```haml
- content_for :header_tags do
  - if user_signed_in?
    -# These can be removed - Vite handles preloading automatically
    -# = preload_pack_asset 'features/compose.js', crossorigin: 'anonymous'
    -# = preload_pack_asset 'features/home_timeline.js', crossorigin: 'anonymous'
```

Additionally, choose performance analysis tools based on testing and proven effectiveness rather than convenience. Tools like rollup-plugin-visualizer may provide better insights than default options for bundle analysis and optimization decisions.