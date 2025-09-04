---
title: Handle optional dependencies gracefully
description: When integrating with external AI libraries, models, or services, handle
  optional dependencies gracefully to avoid affecting users who don't need those features.
  Use local imports within class constructors or methods rather than module-level
  imports, and provide clear error messages when dependencies are missing.
repository: stanfordnlp/dspy
label: AI
language: Python
comments_count: 8
repository_stars: 27813
---

When integrating with external AI libraries, models, or services, handle optional dependencies gracefully to avoid affecting users who don't need those features. Use local imports within class constructors or methods rather than module-level imports, and provide clear error messages when dependencies are missing.

This pattern is essential in AI libraries that integrate with multiple providers (OpenAI, Anthropic, HuggingFace, etc.) where users typically only need a subset of integrations.

Example implementation:
```python
class MistralLM(LM):
    def __init__(self, model: str, **kwargs):
        try:
            import mistralai
        except ImportError as err:
            raise ImportError(
                "The 'mistralai' package is required to use MistralLM. "
                "Install it with 'pip install mistralai'."
            ) from err
        
        super().__init__(model)
        self.client = mistralai.Mistral(api_key=kwargs.get('api_key'))

# Instead of module-level imports that affect everyone:
# import mistralai  # This would cause errors for all users
```

Benefits:
- Users without specific integrations don't encounter import errors
- Clear guidance on how to install missing dependencies  
- Faster import times for the main library
- Easier maintenance as optional dependencies evolve

Apply this pattern consistently across all optional integrations including embedding models, retrieval systems, tracking libraries, and model providers.