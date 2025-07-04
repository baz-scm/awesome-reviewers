---
title: Follow naming conventions
description: "Use consistent and appropriate naming conventions based on the context\
  \ in Python code:\n\n1. **Classes**: Use `CamelCase` for class names\n   ```python\n\
  \   class ResourceMeta(object):"
repository: boto/boto3
label: Naming Conventions
language: Python
comments_count: 7
repository_stars: 9417
---

Use consistent and appropriate naming conventions based on the context in Python code:

1. **Classes**: Use `CamelCase` for class names
   ```python
   class ResourceMeta(object):
       # Class implementation
   ```

2. **Variables and methods**: Use `snake_case` for variables, functions, and methods
   ```python
   self._resource_sub_path = self._resource_name.lower()
   ```

3. **Constants**: Use `UPPER_CASE` for constants
   ```python
   STRING = 'S'
   NUMBER = 'N'
   ```

4. **Private members**: Use leading underscore for internal/private attributes and methods, but avoid redundant underscores when scope already provides privacy
   ```python
   # Good - private method
   def _method_returns_resource_list(resource):
       # Implementation
   
   # Avoid unnecessary underscores for local variables
   def setUp(self):
       patch_global_session = mock.patch('boto3.DEFAULT_SESSION')  # No leading underscore needed
   ```

5. **File naming**: Follow established patterns for file naming
   ```python
   # For test files, use test_<module_name>.py
   test_table.py  # Not test_batch_write.py if testing the table module
   ```

6. **Acronyms**: Properly capitalize acronyms in names
   ```python
   class TestIAMAccessKey(unittest.TestCase):  # Not TestiamAccessKey
   ```

7. **References and paths**: Use snake_case for references and lowercase-hyphenated for URL paths
   ```python
   # For references
   ref.name = 'frob'  # Not 'Frob'
   
   # For URL paths
   self._resource_sub_path = 'service-resource'  # Not 'ServiceResource'
   ```

8. **Type mappings**: Use appropriate Python type names
   ```python
   # Map external types to Python types
   'double': 'float',
   'character': 'string',
   'long': 'integer'
   ```

Consistent naming makes code more readable, maintainable, and reduces cognitive load for developers working with the codebase.