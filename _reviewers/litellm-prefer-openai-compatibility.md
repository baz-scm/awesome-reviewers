---
title: prefer OpenAI compatibility
description: When integrating new LLM providers or AI services, prioritize OpenAI-compatible
  patterns and reuse existing utilities rather than creating separate implementations.
  This approach reduces code duplication, leverages battle-tested functionality, and
  maintains consistency across the codebase.
repository: BerriAI/litellm
label: AI
language: Python
comments_count: 12
repository_stars: 28310
---

When integrating new LLM providers or AI services, prioritize OpenAI-compatible patterns and reuse existing utilities rather than creating separate implementations. This approach reduces code duplication, leverages battle-tested functionality, and maintains consistency across the codebase.

Key practices:
- Add new providers to `openai_compatible_providers` instead of creating separate handler blocks
- Use `base_llm_http_handler` or `openai_like_chat_completion` for OpenAI-compatible APIs
- Inherit from `OpenAILikeConfig` or `OpenAIGPTConfig` for transformation classes
- Reuse existing utilities like `get_llm_provider`, `supports_function_calling`, and parameter mapping functions
- Avoid hardcoding provider-specific logic in main completion functions

Example of preferred approach:
```python
# Instead of creating a separate provider block:
elif custom_llm_provider == "new_provider":
    # Custom implementation...

# Prefer adding to openai_compatible_providers:
openai_compatible_providers = [..., "new_provider"]

# And use existing handlers:
response = base_llm_http_handler.completion(
    model=model,
    messages=messages,
    custom_llm_provider=custom_llm_provider,
    api_base=api_base,
    api_key=api_key,
    # ...
)
```

This pattern ensures new AI integrations benefit from existing error handling, parameter validation, streaming support, and other features while minimizing maintenance overhead.