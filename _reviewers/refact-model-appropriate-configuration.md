---
title: model-appropriate configuration
description: Ensure AI models use configuration settings that match their specific
  architecture and requirements. Different model families (e.g., BigCode vs LLaMA)
  require different tokenizer configurations, memory management settings, and parameter
  mappings. Avoid using generic or copy-pasted configurations across different model
  types.
repository: smallcloudai/refact
label: AI
language: Python
comments_count: 4
repository_stars: 3114
---

Ensure AI models use configuration settings that match their specific architecture and requirements. Different model families (e.g., BigCode vs LLaMA) require different tokenizer configurations, memory management settings, and parameter mappings. Avoid using generic or copy-pasted configurations across different model types.

Key areas to verify:
- **Tokenizer compatibility**: Use correct encoding format and special tokens for the model family
- **Memory management**: Enable checkpointing for large models during training
- **Architecture-specific parameters**: Use appropriate LoRA target modules and freeze exceptions for each model type

Example of proper model-specific configuration:
```python
# Wrong - using BigCode tokenizer config for LLaMA model
"tokenizer": {
    "eot_idx": 0,  # BigCode specific
}

# Right - check model family and use appropriate config
if model_family == "llama":
    tokenizer_config = load_llama_tokenizer_config()
elif model_family == "bigcode":
    tokenizer_config = load_bigcode_tokenizer_config()

# Enable checkpointing for large models
"force_enable_checkpointing": model_size > threshold
```

Always validate that configuration parameters match the target model's architecture to prevent runtime errors and ensure optimal performance.