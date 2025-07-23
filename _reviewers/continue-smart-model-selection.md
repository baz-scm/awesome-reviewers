---
title: Smart model selection
description: 'Implement intelligent model selection mechanisms that adapt to different
  scenarios instead of hardcoding specific AI models. Create abstraction layers that
  can:'
repository: continuedev/continue
label: AI
language: Python
comments_count: 3
repository_stars: 27819
---

Implement intelligent model selection mechanisms that adapt to different scenarios instead of hardcoding specific AI models. Create abstraction layers that can:

1. Automatically select appropriate models based on API key availability
2. Choose models with required capabilities for specific tasks
3. Handle context size limitations with appropriate fallback strategies

For example, instead of directly referencing specific models:

```python
# Avoid this
async for msg_chunk in sdk.models.gpt350613.stream_chat(context, functions=functions):
    # ...

# Prefer this
model = get_model_with_capability("function_calling")
async for msg_chunk in model.stream_chat(context, functions=functions):
    # ...
```

Or implement intelligent upgrade paths:

```python
# Allow models to handle their own upgrades based on context requirements
model_to_use = await model_to_use.maybe_upgrade(required_context_length)
```

This approach makes your AI code more maintainable, adaptable to new models, and cost-efficient while still meeting functional requirements.