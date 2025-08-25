---
title: Configuration parameter validation
description: Always validate configuration parameters for type, range, and reasonable
  values before use. Provide safe defaults for optional settings and prefer explicit
  parameter passing over runtime environment variable modification.
repository: bytedance/deer-flow
label: Configurations
language: Python
comments_count: 3
repository_stars: 16482
---

Always validate configuration parameters for type, range, and reasonable values before use. Provide safe defaults for optional settings and prefer explicit parameter passing over runtime environment variable modification.

Key practices:
- Set conservative defaults for feature flags (disabled by default)
- Validate numeric configuration values are within acceptable ranges
- Use proper logging to report configuration values being applied
- Pass configuration as explicit parameters rather than modifying os.environ at runtime

Example:
```python
# Good: Validate and use safe defaults
recursion_limit = int(os.getenv("AGENT_RECURSION_LIMIT", "25"))
if recursion_limit <= 0:
    raise ValueError("Recursion limit must be greater than zero")
logger.info(f"Recursion limit is set: {recursion_limit}")

# Good: Pass as parameters instead of environment modification
return AzureChatOpenAI(
    api_version=llm_config.get("api_version"),
    api_key=llm_config.get("api_key"),
    azure_endpoint=llm_config.get("base_url")
)

# Avoid: Runtime environment modification
os.environ.update({"AZURE_OPENAI_API_KEY": api_key})  # Not recommended
```