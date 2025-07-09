---
title: Feature flag implementation clarity
description: When implementing feature flags in the system, clearly document both
  the evaluation strategy and its performance implications. For HTTP evaluation vs.
  local evaluation, include expected request volumes and latency impacts. Always provide
  configuration examples that demonstrate proper usage.
repository: neondatabase/neon
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 19015
---

When implementing feature flags in the system, clearly document both the evaluation strategy and its performance implications. For HTTP evaluation vs. local evaluation, include expected request volumes and latency impacts. Always provide configuration examples that demonstrate proper usage.

For example, when implementing a feature flag system:

```
// In your configuration file (e.g., local_proxy.json)
{
  "feature_flags": {
    "evaluation_mode": "local",  // Options: "local", "http"
    "refresh_interval_sec": 60,
    "flags": {
      "gc-compaction": {
        "default": "disabled",
        "variants": ["disabled", "stage-1", "stage-2", "fully-enabled"],
        "filters": {
          "plan_type": ["scale", "enterprise"],
          "min_resident_size_gb": 10,
          "max_resident_size_gb": 100
        }
      }
    }
  }
}
```

Consider performance optimizations when possible. For example, you could map percentage rollouts to tenant ID patterns (e.g., enabling for tenant IDs starting with 0x00 for 1/16th rollout) to allow for easier monitoring via filtering in observability tools.

Document the trade-offs of your chosen approach. For HTTP evaluation, consider the request volume (e.g., "754X requests per month" as noted in one example). For local evaluation, document how often configuration is refreshed and how user properties are evaluated.