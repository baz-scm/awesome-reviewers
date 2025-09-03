---
title: AI provider documentation completeness
description: Ensure comprehensive documentation for AI/ML provider integrations that
  covers all usage patterns, uses precise terminology, and provides helpful context
  for developers.
repository: BerriAI/litellm
label: AI
language: Markdown
comments_count: 9
repository_stars: 28310
---

Ensure comprehensive documentation for AI/ML provider integrations that covers all usage patterns, uses precise terminology, and provides helpful context for developers.

AI provider documentation should include:

1. **Complete usage examples**: Cover SDK usage, proxy configuration, streaming, and advanced features like function calling or image input
2. **Precise terminology**: Use accurate provider-specific terms (e.g., `<hf_org_or_user>/<hf_model>` instead of generic `<model_id>`)
3. **Configuration consistency**: Show both direct API usage and proxy configuration patterns
4. **Provider-specific context**: Explain unique features, billing models, and authentication methods
5. **Missing examples**: Add proxy usage examples when only SDK examples exist

Example of comprehensive documentation structure:
```python
# Basic SDK usage
response = completion(
    model="huggingface/together/deepseek-ai/DeepSeek-R1",
    messages=[{"content": "Hello", "role": "user"}]
)

# Proxy configuration
# config.yaml
model_list:
  - model_name: my-model
    litellm_params:
      model: huggingface/together/deepseek-ai/DeepSeek-R1
      api_key: os.environ/HF_TOKEN
      web_search_options: {}  # Provider-specific options

# Advanced features (when supported)
response = completion(
    model="huggingface/sambanova/Qwen/Qwen2.5-72B-Instruct",
    messages=[{
        "role": "user", 
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {"type": "image_url", "image_url": {"url": "..."}}
        ]
    }]
)
```

This ensures developers have complete guidance for integrating AI providers across different usage patterns and deployment scenarios.