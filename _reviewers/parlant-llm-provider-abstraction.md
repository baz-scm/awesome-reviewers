---
title: LLM provider abstraction
description: When integrating with different LLM providers, create proper base class
  abstractions that filter and validate parameters based on each provider's capabilities.
  Follow established architectural patterns rather than creating custom configuration
  approaches.
repository: emcie-co/parlant
label: AI
language: Python
comments_count: 5
repository_stars: 12205
---

When integrating with different LLM providers, create proper base class abstractions that filter and validate parameters based on each provider's capabilities. Follow established architectural patterns rather than creating custom configuration approaches.

Create provider-specific base classes that define supported parameters and filter hints accordingly. This prevents passing unsupported parameters to APIs and maintains consistency across adapters.

Example implementation:
```python
class OpenAIBaseSchematicGenerator(BaseSchematicGenerator[T], ABC):
    supported_arguments = ["temperature", "logit_bias", "max_tokens"]
    
    async def generate(self, prompt: str, hints: Optional[dict[str, Any]] = None):
        filtered_hints = {}
        if hints:
            for k, v in hints.items():
                if k not in self.supported_arguments:
                    self.logger.warning(f"Key '{k}' is not supported. Skipping...")
                    continue
                filtered_hints[k] = v
        
        response = await self._client.chat.completions.create(
            model=self._get_model_name(),
            **filtered_hints
        )
```

This approach allows code to specify provider requirements ("I want an OpenAI model") while ensuring only valid parameters are passed to each API. Use existing patterns like `CustomSchematicGenerator` and `FallbackSchematicGenerator` rather than implementing custom configuration systems that diverge from established adapter architectures.