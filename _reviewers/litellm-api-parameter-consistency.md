---
title: API parameter consistency
description: Ensure consistent parameter naming, format, and usage across all API
  interfaces, documentation, and code examples. This includes maintaining uniform
  parameter names between SDK examples and proxy configurations, using correct environment
  variable names as specified in official documentation, and applying proper naming
  conventions for model identifiers and...
repository: BerriAI/litellm
label: API
language: Markdown
comments_count: 5
repository_stars: 28310
---

Ensure consistent parameter naming, format, and usage across all API interfaces, documentation, and code examples. This includes maintaining uniform parameter names between SDK examples and proxy configurations, using correct environment variable names as specified in official documentation, and applying proper naming conventions for model identifiers and API routes.

Key areas to verify:
- Model names should include provider prefixes (e.g., `heroku/claude-3-5-haiku`) to enable proper provider identification
- Parameter names must match between SDK examples and proxy configurations (e.g., if SDK uses `api_base`, proxy config should use the same)
- Environment variables should follow official documentation (e.g., `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_BASE_URL` for Anthropic)
- API routes should clearly indicate the underlying service being called (e.g., `openai/responses/<model>` instead of `chat/<model>` for responses API)

Example of consistent parameter usage:
```python
# SDK example
response = completion(
    model="heroku/claude-3-5-haiku",
    api_base="https://us.inference.heroku.com",
    api_key="fake-heroku-key"
)

# Corresponding proxy config should use same parameter names
model_list:
  - model_name: claude-haiku
    litellm_params:
        model: heroku/claude-3-5-haiku
        api_base: https://us.inference.heroku.com
        api_key: fake-heroku-key
```

This consistency prevents confusion, reduces integration errors, and ensures predictable behavior across different usage contexts.