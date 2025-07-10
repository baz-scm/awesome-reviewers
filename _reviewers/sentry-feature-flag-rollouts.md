---
title: Feature flag rollouts
description: Use feature flags to gate new functionality for controlled rollouts.
  This allows for quick enabling/disabling without code reverts when issues arise,
  and supports gradual adoption through percentage-based rollouts.
repository: getsentry/sentry
label: Configurations
language: Python
comments_count: 6
repository_stars: 41297
---

Use feature flags to gate new functionality for controlled rollouts. This allows for quick enabling/disabling without code reverts when issues arise, and supports gradual adoption through percentage-based rollouts.

When implementing a new feature:

1. Create a feature flag or rollout option with a descriptive name
2. Use standard utilities for consistent percentage-based rollouts
3. Design for runtime configuration changes when possible

```python
# Use a descriptive flag name for the specific functionality
register(
    "taskworker.enable_compression.rollout",
    default=0.0,  # Start with 0% rollout
    flags=FLAG_AUTOMATOR_MODIFIABLE,  # Allow runtime changes
)

# In your code, use standard rollout utilities
if features.has("organizations:revoke-org-auth-on-slug-rename", organization):
    # Feature-specific code here
    
# For percentage-based rollouts, use consistent helpers
record_timing_rollout = options.get("sentry.tasks.record.timing.rollout")
if in_random_rollout(record_timing_rollout):
    # Percentage-based rollout code here

# Design for runtime configuration when possible
compression_level = options.get("spans.buffer.compression.level")
zstd_compressor = zstandard.ZstdCompressor(level=compression_level) if compression_level != -1 else None
```

This approach enables safer deployments by allowing features to be rolled out gradually or quickly disabled if issues arise without requiring code reverts.