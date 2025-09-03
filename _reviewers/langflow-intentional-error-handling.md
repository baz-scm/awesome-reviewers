---
title: intentional error handling
description: Make deliberate, context-appropriate decisions about error handling strategy
  rather than applying generic patterns. Consider whether each error scenario should
  fail fast, provide graceful degradation, or offer recovery options based on the
  specific business impact and user experience requirements.
repository: langflow-ai/langflow
label: Error Handling
language: Python
comments_count: 5
repository_stars: 111046
---

Make deliberate, context-appropriate decisions about error handling strategy rather than applying generic patterns. Consider whether each error scenario should fail fast, provide graceful degradation, or offer recovery options based on the specific business impact and user experience requirements.

Key principles:
- **Fail fast for development/configuration errors**: Use explicit failures for issues like missing dependencies, invalid configurations, or programming errors that should be caught early
- **Graceful degradation for optional features**: Allow fallbacks when the failure won't break core functionality, but log appropriately for debugging
- **Avoid silent failures**: Always provide clear feedback about what went wrong and how to fix it
- **Prevent duplicate handling**: Handle errors at the appropriate level to avoid redundant logging and confusing error traces

Example of intentional error handling:
```python
# Fail fast for critical dependencies
try:
    from required_library import CriticalClass
except ImportError as e:
    msg = "Required library not installed. Install with: pip install required_library"
    raise ImportError(msg) from e

# Graceful degradation for optional features  
try:
    dependency_info = analyze_component_dependencies(code)
    metadata["dependencies"] = dependency_info
except (SyntaxError, TypeError, ValueError) as exc:
    logger.warning(f"Failed to analyze dependencies for {name}: {exc}")
    # Continue without dependency info - this is optional
```

The choice between failing fast and graceful degradation should be explicit and documented, considering the impact on users and the ability to debug issues effectively.