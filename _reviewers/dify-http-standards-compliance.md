---
title: HTTP standards compliance
description: Ensure API endpoints follow HTTP standards for status codes and method
  selection. Delete operations should return 204 (No Content) without a response body,
  while update operations should use PUT method instead of GET. This improves API
  consistency and follows REST conventions.
repository: langgenius/dify
label: API
language: Python
comments_count: 5
repository_stars: 114231
---

Ensure API endpoints follow HTTP standards for status codes and method selection. Delete operations should return 204 (No Content) without a response body, while update operations should use PUT method instead of GET. This improves API consistency and follows REST conventions.

For delete operations, use:
```python
def delete(self, member_id):
    # Delete logic here
    return "", 204  # No content, no body
```

For update operations that retrieve and update data:
```python
class ToolMCPUpdateApi(Resource):
    def put(self, provider_id):  # Use PUT instead of GET
        # Update logic here
        return {"result": "success"}, 200
```

Avoid returning response bodies with DELETE methods as per HTTP specifications. Use appropriate status codes: 200 for successful operations with content, 204 for successful operations without content, and proper HTTP methods (GET for retrieval, POST for creation, PUT for updates, DELETE for deletion).