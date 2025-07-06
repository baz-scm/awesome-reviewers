---
title: Backward compatible parameters
description: When evolving API function signatures, maintain backward compatibility
  by making new parameters optional with sensible defaults. This allows existing code
  to continue working while supporting new functionality. When modifying parameters,
  carefully consider the complete data structure being passed, especially for collections
  and complex objects.
repository: bridgecrewio/checkov
label: API
language: Python
comments_count: 3
repository_stars: 7667
---

When evolving API function signatures, maintain backward compatibility by making new parameters optional with sensible defaults. This allows existing code to continue working while supporting new functionality. When modifying parameters, carefully consider the complete data structure being passed, especially for collections and complex objects.

Example:
```python
# Bad: Breaking change - adds required parameter
def run_graph_checks_results(self, runner_filter: RunnerFilter, report_type: str, graph: Graph) -> dict:
    # Implementation

# Good: Backward compatible - new parameter is optional
def run_graph_checks_results(self, runner_filter: RunnerFilter, report_type: str, graph: Graph | None = None) -> dict:
    # Implementation with fallback if graph is None
    
# Bad: Passing incomplete data structure
completion = await openai.ChatCompletion.acreate(
    engine=self.AZURE_OPENAI_DEPLOYMENT_NAME,
    messages=messages[0],  # Only passes first message
)

# Good: Passing complete data structure
completion = await openai.ChatCompletion.acreate(
    engine=self.AZURE_OPENAI_DEPLOYMENT_NAME,
    messages=messages,  # Passes all messages
)
```