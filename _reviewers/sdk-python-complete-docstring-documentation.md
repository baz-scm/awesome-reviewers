---
title: Complete docstring documentation
description: 'Ensure all classes, methods, and properties have comprehensive docstrings
  that clearly explain their purpose, behavior, and usage. Docstrings should be preferred
  over inline comments for method descriptions and should include:'
repository: strands-agents/sdk-python
label: Documentation
language: Python
comments_count: 5
repository_stars: 4044
---

Ensure all classes, methods, and properties have comprehensive docstrings that clearly explain their purpose, behavior, and usage. Docstrings should be preferred over inline comments for method descriptions and should include:

1. **Clear purpose explanation** - What the code does and why it exists
2. **Behavior clarification** - Explain differences in behavior, especially for similar methods
3. **Attribute documentation** - Document all class attributes in the docstring
4. **Examples and expected shapes** - Include usage examples and expected data structures
5. **Parameter and return documentation** - Use proper Args/Returns sections

Example of comprehensive docstring:
```python
class MultiAgentBase(ABC):
    """Base class for multi-agent helpers.

    This class integrates with existing Strands Agent instances and provides
    multi-agent orchestration capabilities.

    Attributes:
        id: Unique identifier for the multi-agent instance
    """

    @property
    def system_prompt(self) -> str | None:
        """Get the system prompt as a string.
        
        Returns the system prompt content converted to string format,
        while system_prompt_content accepts various content types.
        
        Returns:
            String representation of system prompt, or None if not set
        """

def __init__(self, config_source: str | dict[str, any]):
    """Initialize AgentConfig from file path or dictionary.
    
    Args:
        config_source: Either a file path (with 'file://' prefix) or 
                      a dictionary containing agent configuration.
                      Expected shape: {
                          "name": "agent_name",
                          "model": "model_name", 
                          "tools": ["tool1", "tool2"],
                          "system_prompt": "prompt text"
                      }
    """
```

This approach improves code maintainability and helps future contributors understand the codebase without needing to read implementation details or PR discussions.