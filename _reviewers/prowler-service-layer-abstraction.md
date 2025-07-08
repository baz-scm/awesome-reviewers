---
title: Service layer abstraction
description: 'Separate business logic and external service interactions from API views
  by using dedicated service layers. This improves testability, maintainability, and
  enforces separation of concerns in your API design. '
repository: prowler-cloud/prowler
label: API
language: Python
comments_count: 4
repository_stars: 11834
---

Separate business logic and external service interactions from API views by using dedicated service layers. This improves testability, maintainability, and enforces separation of concerns in your API design. 

For example, instead of embedding S3 interactions directly in views:

```python
# Don't do this in your views
@action(detail=True, methods=["get"])
def report(self, request, pk=None):
    s3_client = boto3.client("s3")
    # Direct S3 interaction code...
```

Create a service module:

```python
# services/storage.py
class StorageService:
    def get_report(self, tenant_id, report_id):
        s3_client = self._get_client()
        # S3 interaction code...
        
    def _get_client(self):
        # Client initialization logic
```

Then use it in your views:

```python
@action(detail=True, methods=["get"])
def report(self, request, pk=None):
    storage_service = StorageService()
    report_data = storage_service.get_report(
        request.tenant_id, pk
    )
    # Handle response...
```

When extending existing functionality, reuse common methods rather than creating duplicates with similar behavior. This maintains consistency and reduces maintenance burden across your API.