---
title: Avoid hardcoded API assumptions
description: API interfaces should not contain hardcoded implementation details or
  assume specific underlying technologies. Instead, make them configurable and implementation-agnostic
  to support different backends and configurations.
repository: browser-use/browser-use
label: API
language: Python
comments_count: 2
repository_stars: 69139
---

API interfaces should not contain hardcoded implementation details or assume specific underlying technologies. Instead, make them configurable and implementation-agnostic to support different backends and configurations.

When designing APIs, avoid embedding specific service names, browser types, or implementation details directly in the interface. Use dynamic configuration or parameterization instead.

Example of problematic hardcoded approach:
```python
@self.registry.action(
    'Search the query in Google, the query should be a search query...',
    param_model=SearchGoogleAction,
)

browser = await browser_class.launch(
    headless=self.config.headless,
    channel='chrome',  # Hardcoded despite browser_class potentially being firefox/webkit
)
```

Better approach with configurable implementation:
```python
@self.registry.action(
    f'Search the query in {self.search_engine.title()}, the query should be a search query...',
    param_model=SearchAction,
)

# Use appropriate channel based on browser type or make it configurable
browser = await browser_class.launch(
    headless=self.config.headless,
    channel=self.get_appropriate_channel(browser_class),
)
```

This ensures APIs remain flexible and can adapt to different implementations without requiring interface changes.