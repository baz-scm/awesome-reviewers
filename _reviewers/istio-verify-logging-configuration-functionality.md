---
title: verify logging configuration functionality
description: Ensure that logging configuration options actually perform the behavior
  their names suggest and provide real value. Before implementing or maintaining logging
  features, verify that they work as advertised and aren't just cosmetic labels.
repository: istio/istio
label: Logging
language: Other
comments_count: 2
repository_stars: 37192
---

Ensure that logging configuration options actually perform the behavior their names suggest and provide real value. Before implementing or maintaining logging features, verify that they work as advertised and aren't just cosmetic labels.

This addresses cases where logging configurations appear functional but don't actually control system behavior. For example, a `log_sampled` field that sets a boolean flag but doesn't actually sample requests, or logging policies that exist in code but have no operational impact.

When reviewing logging configurations:
- Test that the configuration actually changes logging behavior
- Verify that field names accurately reflect their function
- Remove or fix configurations that are misleading or non-functional
- Ensure adequate documentation exists for any logging features

Example of problematic configuration:
```json
{
  "log_sampled": "true"  // Misleading - doesn't actually sample, just sets a label
}
```

Rather than maintaining misleading features, either implement proper functionality or remove the configuration entirely. This prevents wasted development effort and user confusion about system behavior.