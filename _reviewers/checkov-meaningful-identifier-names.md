---
title: Meaningful identifier names
description: Choose descriptive and semantic identifiers that clearly convey purpose,
  role, and behavior. Avoid vague, generic names in favor of specific ones that enhance
  code readability and self-documentation.
repository: bridgecrewio/checkov
label: Naming Conventions
language: Python
comments_count: 7
repository_stars: 7667
---

Choose descriptive and semantic identifiers that clearly convey purpose, role, and behavior. Avoid vague, generic names in favor of specific ones that enhance code readability and self-documentation.

Key practices:

1. **Use descriptive names** - Replace generic identifiers with specific ones that reveal intent:
   ```python
   # Poor naming
   new_value = [*vertex.attributes[property], *value]
   
   # Better naming
   list_updated_value = [*vertex.attributes[property], *value]
   ```

2. **Function names should reflect behavior** - Functions should have names that indicate what they do or return:
   ```python
   # Misleading (returns boolean)
   def _prioritise_secrets(secret_records, secret_key, check_id):
       
   # Clear and accurate
   def _should_prioritise_secrets(secret_records, secret_key, check_id):
   ```

3. **Avoid name collisions** - Use prefixes or qualifiers to distinguish similar components:
   ```python
   # Ambiguous - multiple "Runner" classes in codebase
   class Runner(TerraformRunner):
       
   # Clear and specific
   class TerraformJsonRunner(TerraformRunner):
   ```

4. **Use consistent naming patterns** - Maintain consistent naming styles for similar concepts:
   ```python
   # Inconsistent
   self.dataflow = data_flow
   
   # Consistent
   self.data_flow = data_flow
   ```

5. **Disambiguate from standard library** - When naming functions that might conflict with standard functions, use clarifying prefixes:
   ```python
   # Potentially confusing with standard library
   def deepcopy(obj: _T) -> _T:
       
   # Clear it's a custom implementation
   def pickle_deepcopy(obj: _T) -> _T:
   ```

When iterating over collections, use descriptive variable names instead of generic ones:
```python
# Vague
for each in resource_changes:
    # ...

# Descriptive
for changed_resource in resource_changes:
    # ...
```