---
title: Complete model configurations
description: When adding new models to configuration files, ensure all required configuration
  fields are populated, not just the model name in the running_models list. Models
  need complete configuration in both JSON (known_models.json) and YAML (provider
  files) with all necessary fields specified.
repository: smallcloudai/refact
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 3114
---

When adding new models to configuration files, ensure all required configuration fields are populated, not just the model name in the running_models list. Models need complete configuration in both JSON (known_models.json) and YAML (provider files) with all necessary fields specified.

Required fields typically include:
- `n_ctx`: Context window size
- `supports_tools`: Tool calling capability
- `supports_multimodality`: Image/file support
- `supports_agent`: Agent functionality
- `tokenizer`: Tokenizer path
- Additional provider-specific fields

Example of complete configuration:

```yaml
# In provider YAML file
running_models:
  - claude-4

chat_models:
  claude-4:
    n_ctx: 200000
    supports_tools: true
    supports_multimodality: true
    supports_clicks: true
    supports_agent: true
    supports_reasoning: anthropic
    tokenizer: hf://Xenova/claude-tokenizer
```

Incomplete configurations where only the model name is added to `running_models` without corresponding detailed configuration will result in runtime errors or unexpected behavior. Always cross-reference known_models.json to understand which configuration fields are required for proper model functionality.