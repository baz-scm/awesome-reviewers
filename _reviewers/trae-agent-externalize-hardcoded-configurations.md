---
title: Externalize hardcoded configurations
description: Configuration values should be externalized to environment variables
  rather than hardcoded in the source code. This improves flexibility, security, and
  deployment across different environments.
repository: bytedance/trae-agent
label: Configurations
language: Python
comments_count: 2
repository_stars: 9088
---

Configuration values should be externalized to environment variables rather than hardcoded in the source code. This improves flexibility, security, and deployment across different environments.

Hardcoded configuration values make applications inflexible and difficult to deploy across different environments. Instead, use environment variables with sensible defaults.

Example of the improvement:
```python
# Bad: Hardcoded configuration
self.client = openai.OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434"
)

# Good: Environment-configurable
self.client = openai.OpenAI(
    api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
    base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434")
)
```

This approach allows the same code to work in development, testing, and production environments by simply changing environment variables, without requiring code modifications or rebuilds.