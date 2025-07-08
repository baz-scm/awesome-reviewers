---
title: Preserve API compatibility
description: When modifying API interfaces, parameters, or argument behavior, ensure
  backward compatibility is maintained to prevent breaking existing user code. If
  a parameter needs to be renamed or enhanced, continue supporting the old parameter
  name alongside the new one.
repository: vllm-project/vllm
label: API
language: Python
comments_count: 5
repository_stars: 51730
---

When modifying API interfaces, parameters, or argument behavior, ensure backward compatibility is maintained to prevent breaking existing user code. If a parameter needs to be renamed or enhanced, continue supporting the old parameter name alongside the new one.

For example, when expanding API parameters to support new functionality:

```python
# GOOD: Maintain backward compatibility
class ScoreRequest(OpenAIBaseModel):
    model: Optional[str] = None
    # Keep old parameter names to maintain compatibility
    text_1: Optional[Union[list[str], str]] = None
    text_2: Optional[Union[list[str], str]] = None
    # Add new parameters with enhanced functionality
    data_1: Optional[Union[list[str], str, ScoreMultiModalParam]] = None
    data_2: Optional[Union[list[str], str, ScoreMultiModalParam]] = None
    
    def __post_init__(self):
        # Use old parameters if new ones aren't provided
        if self.data_1 is None and self.text_1 is not None:
            self.data_1 = self.text_1
        if self.data_2 is None and self.text_2 is not None:
            self.data_2 = self.text_2
```

When removing or changing interface methods, first mark them as deprecated and provide clear migration guidance. For public APIs, follow a formal deprecation policy with adequate notice before removal. For internal APIs with multiple consumers, coordinate changes to ensure dependent systems aren't broken.

Always document your API changes thoroughly, including:
1. What changed and why
2. How existing users should migrate their code
3. When deprecated features will be removed (if applicable)