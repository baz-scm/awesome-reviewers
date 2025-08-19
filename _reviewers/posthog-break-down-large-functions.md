---
title: break down large functions
description: Large functions that handle multiple responsibilities should be decomposed
  into smaller, focused functions to improve readability, maintainability, and facilitate
  code reviews.
repository: PostHog/posthog
label: Code Style
language: Python
comments_count: 5
repository_stars: 28460
---

Large functions that handle multiple responsibilities should be decomposed into smaller, focused functions to improve readability, maintainability, and facilitate code reviews.

When a function becomes difficult to understand at a glance or handles multiple distinct operations, consider extracting logical chunks into separate methods. This is especially important when functions exceed ~50 lines or when reviewers comment that the code would benefit from splitting.

**Example of improvement:**
```python
# Before: Large function doing multiple things
def _process_insight_for_evaluation(self, insight: Insight, query_executor: AssistantQueryExecutor) -> dict:
    insight_info = self._create_base_insight_info(insight)
    
    try:
        query_dict = self._parse_insight_query(insight)
        if query_dict:
            self._execute_and_update_info(insight_info, query_dict, query_executor)
            self._add_visualization_message(insight_info, insight)
        else:
            self._handle_no_query(insight_info, insight)
    except Exception as e:
        self._handle_evaluation_error(insight_info, insight, e)
    
    return insight_info

# After: Broken into focused helper methods
def _parse_insight_query(self, insight: Insight) -> dict | None:
    # Separate method for query parsing
    pass

def _execute_and_update_info(self, insight_info: dict, query_dict: dict, executor):
    # Separate method for execution
    pass
```

This approach makes each function easier to test, understand, and modify independently. It also makes code reviews more focused since reviewers can evaluate each logical operation separately.