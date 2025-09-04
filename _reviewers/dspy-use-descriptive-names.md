---
title: Use descriptive names
description: Choose variable, method, class, and parameter names that clearly communicate
  their purpose and avoid ambiguity. Names should be self-documenting and specific
  rather than generic or vague.
repository: stanfordnlp/dspy
label: Naming Conventions
language: Python
comments_count: 11
repository_stars: 27813
---

Choose variable, method, class, and parameter names that clearly communicate their purpose and avoid ambiguity. Names should be self-documenting and specific rather than generic or vague.

**Key principles:**
- **Be specific about purpose**: Use `max_parse_retries` instead of `adapter_retry_count`, or `should_document_method` instead of `is_documented_method`
- **Avoid generic names**: Replace vague names like `InputField` or `enumerate_fields` with descriptive ones like `UserProfile` or `get_field_description_string`
- **Use meaningful variable names**: Instead of confusing names like `input_opt_right` and `input_opt_left`, use clear names like `input1` and `input2` with explanatory comments
- **Be consistent across functions**: If using `train_method` in one function, use it consistently rather than switching to `method` elsewhere

**Example:**
```python
# Poor naming - vague and confusing
def enumerate_fields(fields: dict) -> str:
    adapter_retry_count = 0
    input_opt_right = "test"
    
# Better naming - descriptive and clear  
def get_field_description_string(fields: dict) -> str:
    max_parse_retries = 0
    user_input = "test"
```

This approach makes code more maintainable and reduces the cognitive load for other developers reading your code.