---
title: Preserve unset field values
description: When implementing partial updates in FastAPI, use the `exclude_unset`
  parameter in Pydantic's `.dict()` or `.model_dump()` method to avoid overriding
  existing values with defaults. This ensures that only fields explicitly set by the
  client are updated, while preserving any existing values for fields not included
  in the request. This pattern is particularly...
repository: fastapi/fastapi
label: Null Handling
language: Markdown
comments_count: 3
repository_stars: 86871
---

When implementing partial updates in FastAPI, use the `exclude_unset` parameter in Pydantic's `.dict()` or `.model_dump()` method to avoid overriding existing values with defaults. This ensures that only fields explicitly set by the client are updated, while preserving any existing values for fields not included in the request. This pattern is particularly useful for PATCH operations.

```python
@app.patch("/items/{item_id}")
def update_item(item_id: str, item: Item):
    # Retrieve the existing item from storage
    stored_item = get_stored_item(item_id)
    stored_item_model = Item(**stored_item)
    
    # Get only the fields that were set in the request
    update_data = item.dict(exclude_unset=True)  # or .model_dump(exclude_unset=True) in Pydantic v2
    
    # Update the stored model, preserving fields not explicitly set
    updated_item = stored_item_model.copy(update=update_data)
    
    # Convert the updated model to a format suitable for storage
    return updated_item
```

By using `exclude_unset=True`, you prevent accidentally resetting fields to default values when they weren't included in the request body. This approach respects null handling principles by distinguishing between fields that were explicitly set to null and fields that were simply not included in the request.