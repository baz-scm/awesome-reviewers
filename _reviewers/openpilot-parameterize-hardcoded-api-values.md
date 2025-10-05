---
title: Parameterize hardcoded API values
description: When designing APIs or interfaces, avoid hardcoding string literals,
  configuration values, or identifiers that could be made configurable through parameters.
  This makes the API more flexible, reusable, and maintainable by allowing callers
  to specify their own values rather than being locked into fixed behavior.
repository: commaai/openpilot
label: API
language: Other
comments_count: 2
repository_stars: 58214
---

When designing APIs or interfaces, avoid hardcoding string literals, configuration values, or identifiers that could be made configurable through parameters. This makes the API more flexible, reusable, and maintainable by allowing callers to specify their own values rather than being locked into fixed behavior.

Hardcoded values in APIs create tight coupling and reduce reusability. Instead, expose these values as parameters in your interface design, allowing different use cases to be supported without code changes.

Example of the problem:
```cpp
// Bad: hardcoded "thumbnail" string
pm.reset(new PubMaster({encoder_info.publish_name, "thumbnail"}));
```

Better approach:
```cpp
// Good: parameterize the thumbnail name through EncoderInfo
pm.reset(new PubMaster({encoder_info.publish_name, encoder_info.thumbnail_name}));
```

This principle applies to API endpoints, configuration keys, default values, and any identifier that might need to vary across different contexts or use cases. By parameterizing these values, you create more flexible interfaces that can adapt to different requirements without requiring code modifications.