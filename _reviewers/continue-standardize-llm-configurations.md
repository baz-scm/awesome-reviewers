---
title: Standardize LLM configurations
description: When configuring LLM providers and their capabilities, always use proper
  JSON syntax with quoted property names and explicitly declare all relevant capabilities.
  This ensures your AI models work as expected with the correct features enabled.
repository: continuedev/continue
label: AI
language: Markdown
comments_count: 3
repository_stars: 27819
---

When configuring LLM providers and their capabilities, always use proper JSON syntax with quoted property names and explicitly declare all relevant capabilities. This ensures your AI models work as expected with the correct features enabled.

For third-party LLM providers:
1. Always use quoted property names in JSON configuration
2. Explicitly declare all model capabilities that are needed
3. Verify configuration file paths and formats are correct

Example of proper LLM configuration:

```json
{
  "models": [
    {
      "title": "Custom Provider",
      "provider": "openai",
      "model": "third-party-model",
      "contextLength": 8192,
      "apiBase": "https://your-api-provider/v1",
      "capability": {
        "uploadImage": true,
        "tools": true
      }
    }
  ]
}
```

Proper configuration prevents runtime errors when using AI features and ensures that all capabilities (like image uploads or tool use) are correctly recognized by the system.