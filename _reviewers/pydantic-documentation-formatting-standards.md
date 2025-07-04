---
title: Documentation formatting standards
description: 'Maintain consistent documentation formatting to ensure proper rendering
  and readability. Follow these key practices:


  1. **Consistent code output display**: Standardize how objects are printed in examples.
  Either use `print(<inst>)` or `print(repr(<inst>))` consistently throughout the
  documentation.'
repository: pydantic/pydantic
label: Code Style
language: Markdown
comments_count: 3
repository_stars: 24377
---

Maintain consistent documentation formatting to ensure proper rendering and readability. Follow these key practices:

1. **Consistent code output display**: Standardize how objects are printed in examples. Either use `print(<inst>)` or `print(repr(<inst>))` consistently throughout the documentation.

2. **Proper markdown list formatting**: 
   - Always include a blank line after a list item when followed by a code block
   - Use 4-space indentation (not 2 or 3) for code blocks within lists to ensure proper rendering
   
3. **Newline consistency**: Be mindful of how newlines affect rendering, especially in lists and admonitions.

Example of proper markdown list formatting with code:

```markdown
- List item with code example:

    ```python
    from pydantic import BaseModel
    
    class Example(BaseModel):
        field: str
        
    print(Example(field="value"))
    ```
```

Following these standards will prevent broken documentation rendering and maintain a consistent look and feel throughout the codebase.