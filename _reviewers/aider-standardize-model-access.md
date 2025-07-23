---
title: Standardize model access
description: 'When integrating AI models into applications, provide consistent configuration
  methods that support different access patterns (direct API, chat interfaces, or
  intermediary services like LiteLLM). '
repository: Aider-AI/aider
label: AI
language: Python
comments_count: 3
repository_stars: 35856
---

When integrating AI models into applications, provide consistent configuration methods that support different access patterns (direct API, chat interfaces, or intermediary services like LiteLLM). 

Key practices:
1. Support environment variables for flexible configuration (e.g., `LITELLM_BASE_URL`, `OPENAI_API_KEY`)
2. Handle both local and remote model access scenarios
3. Account for behavioral differences between chat and API modes of the same model
4. Use clear prefixing for different interaction modes

Example:
```python
def create_model(model_name, **kwargs):
    # Support prefix-based mode selection
    COPY_PASTE_PREFIX = "cp:"
    copy_paste_mode = model_name.startswith(COPY_PASTE_PREFIX)
    if copy_paste_mode:
        model_name = model_name.removeprefix(COPY_PASTE_PREFIX)
    
    # Support environment variables for configuration
    base_url = os.environ.get("MODEL_API_BASE_URL")
    api_key = os.environ.get("MODEL_API_KEY")
    
    # Create appropriate client based on configuration
    if base_url:
        client = RemoteModelClient(base_url, api_key, model_name)
    else:
        client = LocalModelClient(model_name)
        
    return client
```

This standardized approach improves maintainability when supporting multiple AI backends and simplifies switching between different deployment configurations.