---
title: User-friendly configuration retrieval
description: When retrieving configuration values like API keys or environment variables,
  include helpful error messages that guide users on how to fix missing configurations.
  Consider centralizing configuration retrieval logic in the appropriate classes based
  on their usage patterns.
repository: continuedev/continue
label: Configurations
language: Python
comments_count: 2
repository_stars: 27819
---

When retrieving configuration values like API keys or environment variables, include helpful error messages that guide users on how to fix missing configurations. Consider centralizing configuration retrieval logic in the appropriate classes based on their usage patterns.

For example, instead of just reporting a missing environment variable:

```python
# Better approach with helpful guidance
async def get_api_key(self, env_var: str) -> str:
    # Provide a helpful default message that references the specific environment variable
    prompt = f"Please add your {env_var} to the .env file"
    return await self.ide.getUserSecret(env_var, prompt=prompt)
```

This approach not only handles the configuration retrieval but also improves developer experience by providing clear guidance when configuration issues arise. For configuration logic that's specific to certain components (like Models), consider housing that logic within those component classes rather than in general utility methods.