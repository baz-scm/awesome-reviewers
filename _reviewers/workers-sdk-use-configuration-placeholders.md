---
title: Use configuration placeholders
description: Configuration files should use placeholder values like `<TBD>` instead
  of hardcoded values for fields that need to be dynamically replaced by tooling or
  build processes. This ensures that automated systems can properly substitute the
  correct values during project setup or deployment.
repository: cloudflare/workers-sdk
label: Configurations
language: Toml
comments_count: 2
repository_stars: 3379
---

Configuration files should use placeholder values like `<TBD>` instead of hardcoded values for fields that need to be dynamically replaced by tooling or build processes. This ensures that automated systems can properly substitute the correct values during project setup or deployment.

Hardcoded values prevent tooling from functioning correctly and can lead to inconsistencies between user selections and final configuration. For example, if a user selects the project name "crimson-sky-1234" but the configuration contains a hardcoded name, the final result won't match their choice.

Example of correct placeholder usage:
```toml
name = "<TBD>"
compatibility_date = "<TBD>"
```

Instead of:
```toml
name = "hello-python-worker"
compatibility_date = "2024-03-20"
```

This practice allows build tools to automatically look up the latest compatibility dates and apply user-specified names, ensuring configurations remain current and personalized.