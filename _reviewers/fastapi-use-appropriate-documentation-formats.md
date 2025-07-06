---
title: Use appropriate documentation formats
description: "Choose the most suitable documentation format based on context to maximize\
  \ readability and information value. \n\nFor Pydantic models:\n- Use class-level\
  \ docstrings for comprehensive documentation that supports rich formatting including\
  \ newlines and emphasis"
repository: fastapi/fastapi
label: Documentation
language: Python
comments_count: 2
repository_stars: 86871
---

Choose the most suitable documentation format based on context to maximize readability and information value. 

For Pydantic models:
- Use class-level docstrings for comprehensive documentation that supports rich formatting including newlines and emphasis
- Use Field descriptions for specific field-level details
- Include line breaks in longer descriptions to improve readability

**Example:**
```python
class Item(BaseModel):
    """Description of the model.
    
    This allows more formatting than field descriptions like
    
    newlines, *emphasis*.
    """
    id: str = Field(
        title="Short title of the field",
        description="Longer description what the field is used for.\n\nUse line breaks for readability.",
    )
```

This approach provides consistent and well-structured documentation that's readable both in source code and in generated API documentation.