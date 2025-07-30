---
title: Database schema compliance
description: Ensure database integrations use correct field names, data types, and
  schema conventions specific to each database system. Different databases have special
  field naming requirements and data type expectations that must be respected to avoid
  runtime errors and ensure proper functionality.
repository: Unstructured-IO/unstructured
label: Database
language: Python
comments_count: 4
repository_stars: 12117
---

Ensure database integrations use correct field names, data types, and schema conventions specific to each database system. Different databases have special field naming requirements and data type expectations that must be respected to avoid runtime errors and ensure proper functionality.

Key considerations:
- Research database-specific field naming conventions (e.g., `$vector` for embeddings in Astra DB, `_id` for document identifiers)
- Convert data types appropriately for database storage (e.g., timestamps as integers for file modification times)
- Validate schema requirements during development and testing
- Use database-native field names in normalization methods

Example from Astra DB integration:
```python
def normalize_dict(self, element_dict: dict) -> dict:
    return {
        "_id": str(uuid.uuid4()),  # Astra DB expects _id, not id
        "$vector": element_dict.pop("embeddings", None),  # Special $vector field
        "content": element_dict.pop("text", None),
        "metadata": element_dict,
    }
```

This prevents issues like vector search failures due to incorrect field naming and ensures data is stored in the format expected by the target database system.