---
title: Explicit configuration validation
description: Avoid using configuration values as implicit feature flags or logic triggers.
  Instead, validate configuration explicitly and make behavior predictable.
repository: SWE-agent/SWE-agent
label: Configurations
language: Python
comments_count: 5
repository_stars: 16839
---

Avoid using configuration values as implicit feature flags or logic triggers. Instead, validate configuration explicitly and make behavior predictable.

Configuration values should not be used to implicitly detect features or modes of operation, as this leads to false positives/negatives and confusing behavior. When configuration is required, validate it explicitly and fail fast with clear error messages.

**Problems to avoid:**
- Using cost limits of 0 to detect local models: `if self.config.per_instance_cost_limit == 0 and self.config.total_cost_limit == 0: # Local model`
- Allowing missing required configuration to silently fall back to defaults that may not work
- Using configuration values in complex conditional logic that's hard to reason about

**Better approach:**
```python
# Instead of implicit detection
if self.config.per_instance_cost_limit == 0 and self.config.total_cost_limit == 0:
    # Local model logic

# Use explicit configuration
if self.config.model_type == "local":
    # Local model logic

# Validate required configuration explicitly
if self.args.model_name.startswith("deepseek"):
    api_base_url = keys_config.get("DEEPSEEK_API_BASE_URL")
    if not api_base_url:
        raise ValueError("DEEPSEEK_API_BASE_URL must be specified for DeepSeek models")
```

Make configuration behavior predictable by validating requirements upfront and using explicit flags rather than inferring behavior from side effects of other configuration values.