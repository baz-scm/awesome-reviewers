---
title: Maintain configuration consistency
description: When modifying configuration settings, especially environment variables,
  ensure changes are consistent with existing codebase usage patterns and maintain
  backward compatibility. Before changing configuration names or values, audit the
  codebase to understand current usage and dependencies.
repository: browser-use/browser-use
label: Configurations
language: Other
comments_count: 2
repository_stars: 69139
---

When modifying configuration settings, especially environment variables, ensure changes are consistent with existing codebase usage patterns and maintain backward compatibility. Before changing configuration names or values, audit the codebase to understand current usage and dependencies.

For environment variables, check how they are referenced throughout the application, including tests, documentation, and third-party integrations. Consider that different libraries may expect different variable names for the same functionality.

Example from Azure OpenAI configuration:
```python
# Check existing usage before changing variable names
return AzureChatOpenAI(
    model='gpt-4o',
    api_version='2024-10-21',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
    api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', '')),  # Keep existing name
)
```

For related configuration values, ensure they are compatible with each other. For instance, when setting viewport and window sizes, account for UI chrome and ensure viewport dimensions don't exceed window dimensions to prevent content cutoff.