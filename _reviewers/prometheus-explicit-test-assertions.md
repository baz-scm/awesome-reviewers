---
title: explicit test assertions
description: Tests should explicitly assert both positive and negative expectations
  to make test intentions clear and prevent regressions. Use the `expect` syntax to
  specify not only what should happen, but also what should NOT happen in your tests.
repository: prometheus/prometheus
label: Testing
language: Other
comments_count: 5
repository_stars: 59616
---

Tests should explicitly assert both positive and negative expectations to make test intentions clear and prevent regressions. Use the `expect` syntax to specify not only what should happen, but also what should NOT happen in your tests.

When testing scenarios that should produce warnings or info messages, use `expect warn` or `expect info`. Equally important, when testing scenarios that should NOT produce these annotations, use `expect no_warn` or `expect no_info` to make this expectation explicit.

This approach serves two purposes:
1. **Clarity**: Future developers can immediately understand what the test is validating
2. **Regression prevention**: Changes that accidentally introduce or remove annotations will be caught

Example:
```
# Explicit about expecting a warning
eval instant at 20m irate(http_requests_histogram{path="/c"}[20m])
    expect warn
    {path="/c"} {{sum:0.01 count:0.01 counter_reset_hint:gauge}}

# Explicit about NOT expecting a warning  
eval instant at 20m irate(http_requests_histogram{path="/f"}[20m])
    expect no_warn
    {path="/f"} {{schema:-53 sum:0.01 count:0.01 custom_values:[5 10] buckets:[0.01]}}
```

Remember: the old `eval` behavior always asserted no annotations, but the new behavior is more tolerant. Be explicit about your expectations to maintain test robustness.