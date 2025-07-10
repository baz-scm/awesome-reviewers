---
title: Consider related object cleanup
description: When implementing migration operations that modify or remove database
  objects like fields and models, ensure all related objects (indexes, constraints,
  foreign keys) are properly identified and removed. Failing to handle these dependencies
  can leave orphaned database objects that may cause issues later.
repository: django/django
label: Migrations
language: Python
comments_count: 3
repository_stars: 84182
---

When implementing migration operations that modify or remove database objects like fields and models, ensure all related objects (indexes, constraints, foreign keys) are properly identified and removed. Failing to handle these dependencies can leave orphaned database objects that may cause issues later.

When removing fields, check for dependencies like indexes or constraints that reference those fields:

```python
# Example: Ensuring indexes are removed when removing fields
# Note how dependencies are explicitly defined for field removal

def _generate_removed_field(self, app_label, model_name, field_name):
    # Include dependencies such as order_with_respect_to, constraints,
    # and any generated fields that may depend on this field
    dependencies = [
        OperationDependency(
            app_label,
            model_name,
            field_name,
            OperationDependency.Type.REMOVE_INDEX_OR_CONSTRAINT,
        ),
        # Add other dependencies as needed
    ]
    
    # Add the operation with proper dependencies
    self.add_operation(
        app_label,
        operations.RemoveField(
            model_name=model_name,
            name=field_name,
        ),
        dependencies=dependencies,
    )
```

Write tests that verify the proper cleanup of related objects when fields or models are removed. This is especially important for complex relationships between models.