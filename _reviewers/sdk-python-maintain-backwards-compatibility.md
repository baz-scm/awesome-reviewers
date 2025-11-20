---
title: maintain backwards compatibility
description: When modifying public APIs, always preserve backwards compatibility to
  avoid breaking existing consumers. Public methods, even if rarely used directly,
  must maintain their existing signatures and behavior.
repository: strands-agents/sdk-python
label: API
language: Python
comments_count: 8
repository_stars: 4044
---

When modifying public APIs, always preserve backwards compatibility to avoid breaking existing consumers. Public methods, even if rarely used directly, must maintain their existing signatures and behavior.

Use these patterns to evolve APIs safely:

**Add new methods instead of modifying existing ones:**
```python
# Instead of changing invoke_callbacks() to async
def invoke_callbacks(self, event: TInvokeEvent) -> tuple[TInvokeEvent, list[Interrupt]]:
    # Keep existing sync method
    
async def invoke_callbacks_async(self, event: TInvokeEvent) -> tuple[TInvokeEvent, list[Interrupt]]:
    # Add new async method, deprecate old one
```

**Use parameter separators for new optional parameters:**
```python
# Backwards compatible - new params after *
def __call__(
    self, prompt: AgentInput = None, *, 
    structured_output_type: Type[BaseModel] | None = None, 
    **kwargs: Any
) -> AgentResult:
```

**Avoid @abstractmethod for new interface methods:**
```python
# Breaking - forces all implementers to update immediately
@abstractmethod
def new_method(self): pass

# Non-breaking - allows gradual adoption
def new_method(self):
    raise NotImplementedError("Subclasses should implement this method")
```

**Preserve import paths when reorganizing:**
```python
# In __init__.py - maintain old import while moving implementation
from .new_location import convert_pydantic_to_tool_spec
```

Consider the impact on all consumers, including those calling public methods directly, extending abstract classes, or using specific import paths. When in doubt, add new APIs alongside existing ones rather than modifying them.