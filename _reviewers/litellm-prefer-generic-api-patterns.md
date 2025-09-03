---
title: Prefer generic API patterns
description: Avoid creating provider-specific API implementations when generic, reusable
  solutions exist or can be developed. This principle improves code maintainability,
  reduces duplication, and ensures consistency across the API surface.
repository: BerriAI/litellm
label: API
language: Python
comments_count: 5
repository_stars: 28310
---

Avoid creating provider-specific API implementations when generic, reusable solutions exist or can be developed. This principle improves code maintainability, reduces duplication, and ensures consistency across the API surface.

Key practices:
- Reuse existing handlers and base classes instead of creating new ones
- Avoid hardcoded API endpoints; use configurable base URLs
- Register providers in existing systems rather than adding custom routing logic
- Create generic parameter handling that works across multiple providers

Example from the discussions:
```python
# Instead of creating a new handler:
class HostedVLLMRerank(BaseLLM):
    # custom implementation...

# Reuse existing patterns:
# "please follow the cohere integration, and use the base_llm_http_handler"

# Instead of hardcoded endpoints:
if "gateway.ai.cloudflare.com" in api_base:
    # custom logic...

# Use generic configuration:
api_base = api_base or get_configurable_base_url()
```

This approach reduces technical debt, makes the codebase more predictable for developers, and ensures that improvements to core functionality benefit all providers rather than being siloed in provider-specific implementations.