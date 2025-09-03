---
title: AI model data validation
description: All AI model configuration parameters must be verified against official
  provider documentation before merging. This includes token limits, pricing values,
  provider assignments, model names, and supported features. Incorrect configuration
  data leads to runtime errors, cost miscalculations, and integration failures.
repository: BerriAI/litellm
label: AI
language: Json
comments_count: 11
repository_stars: 28310
---

All AI model configuration parameters must be verified against official provider documentation before merging. This includes token limits, pricing values, provider assignments, model names, and supported features. Incorrect configuration data leads to runtime errors, cost miscalculations, and integration failures.

Key validation requirements:
- Verify max_input_tokens, max_output_tokens against official docs (e.g., "Should this be 65535 per Google's documentation?")
- Validate pricing using scientific notation and correct per-token costs (e.g., "The pricing `0.00021` is incorrect. It's 0.21/1m tokens")
- Ensure provider field matches actual API provider (e.g., "provider should be `bedrock_converse`" not "bedrock")
- Confirm model names match those returned by provider APIs for accurate cost tracking
- Use proper JSON formatting (true/false, not True/False)

Example of proper validation:
```json
"gpt-5-2025-08-07": {
    "max_input_tokens": 272000,  // Verified against OpenAI docs
    "input_cost_per_token": 1.25e-06,  // Scientific notation, verified pricing
    "litellm_provider": "openai",  // Matches actual API provider
    "supports_function_calling": true  // JSON boolean, not Python
}
```

Always include source citations when making configuration changes to enable future verification and maintain data integrity.