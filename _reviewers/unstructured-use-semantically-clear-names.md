---
title: Use semantically clear names
description: Choose variable, method, and class names that clearly express their purpose
  and functionality to avoid confusion and improve code readability. Names should
  accurately reflect what the code does rather than how it's implemented.
repository: Unstructured-IO/unstructured
label: Naming Conventions
language: Python
comments_count: 12
repository_stars: 12117
---

Choose variable, method, and class names that clearly express their purpose and functionality to avoid confusion and improve code readability. Names should accurately reflect what the code does rather than how it's implemented.

**Key principles:**
- **Avoid misleading names**: Don't use names that suggest different functionality than what they provide
- **Be descriptive**: Use specific, meaningful names rather than generic or abbreviated ones  
- **Match intent**: Ensure the name reflects the actual purpose, not implementation details

**Examples:**

```python
# ❌ Misleading - sounds like it creates an index
def create_index(self) -> "PineconeIndex":
    return existing_index

# ✅ Clear - indicates it retrieves an existing index  
def get_index(self) -> "PineconeIndex":
    return existing_index

# ❌ Ambiguous abbreviation
def group_text_extraction_acc():
    pass

# ✅ Explicit and clear
def group_text_extraction_accuracy():
    pass

# ❌ Generic and unclear purpose
def write_raw_dict(self, elements_dict):
    self.normalize_data(elements_dict)
    self.write_to_db(elements_dict)

# ✅ Describes what the method actually does
def normalize_and_write_dict(self, elements_dict):
    self.normalize_data(elements_dict) 
    self.write_to_db(elements_dict)

# ❌ Predicate named like a function
skip_outside_ci = os.getenv("CI", "").lower() in {"", "false", "f", "0"}

# ✅ Boolean variable with clear intent
is_in_ci = os.getenv("CI", "").lower() not in {"", "false", "f", "0"}
```

This approach reduces cognitive load for developers, makes code self-documenting, and prevents misunderstandings about functionality.