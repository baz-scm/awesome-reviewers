---
title: eliminate code duplication
description: Identify and consolidate duplicate code patterns by extracting common
  logic into reusable functions and unifying similar code blocks. This improves maintainability,
  reduces bugs, and enhances readability.
repository: strands-agents/sdk-python
label: Code Style
language: Python
comments_count: 7
repository_stars: 4044
---

Identify and consolidate duplicate code patterns by extracting common logic into reusable functions and unifying similar code blocks. This improves maintainability, reduces bugs, and enhances readability.

Key strategies:
- **Unify similar conditional blocks**: Instead of having separate if/else branches with identical content, create a single path that handles both cases
- **Extract common logic**: Move repeated code into helper functions with descriptive names
- **Eliminate redundant checks**: Remove unnecessary repeated validations or state checks within the same method
- **Simplify complex expressions**: Break down complex inline constructions into separate, reusable components

Example from the codebase:
```python
# Before: Duplicate code paths
if self.node_timeout is not None:
    events = self._stream_with_timeout(...)
else:
    events = self.stream_async(...)

# After: Unified approach
events = self._stream_with_timeout(...) if self.node_timeout else self.stream_async(...)
```

Another example:
```python
# Before: Complex inline construction
after_event = agent.hooks.invoke_callbacks(
    AfterToolCallEvent(
        agent=agent,
        tool_use=tool_use,
        result={
            "toolUseId": tool_use["toolUseId"],
            "status": "cancelled",
            "content": [{"text": "Tool execution was cancelled"}]
        }
    )
)

# After: Extract result construction
cancelled_result = self._create_cancelled_tool_result(tool_use)
after_event = agent.hooks.invoke_callbacks(
    AfterToolCallEvent(agent=agent, tool_use=tool_use, result=cancelled_result)
)
```

Always look for opportunities to consolidate when you notice similar patterns, repeated logic, or multiple code paths that achieve the same outcome.