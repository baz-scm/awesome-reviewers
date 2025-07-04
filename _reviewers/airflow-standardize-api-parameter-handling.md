---
title: Standardize API parameter handling
description: 'Use consistent parameter handling patterns across API endpoints to ensure
  maintainability and predictable behavior. Follow these guidelines:


  1. Use FastAPI''s native parameter handling for lists:'
repository: apache/airflow
label: API
language: Python
comments_count: 6
repository_stars: 40858
---

Use consistent parameter handling patterns across API endpoints to ensure maintainability and predictable behavior. Follow these guidelines:

1. Use FastAPI's native parameter handling for lists:
```python
# Good
def get_dependencies(
    node_ids: list[str] | None = Query(None)
) -> BaseGraphResponse:
    pass

# Avoid
def get_dependencies(
    node_ids: str | None = Query(None, description="Comma-separated list of node ids")
) -> BaseGraphResponse:
    ids_to_fetch = [nid.strip() for nid in node_ids.split(",")] if node_ids else []
```

2. Define constants for query parameter limits:
```python
MAX_SORT_PARAMS = 2

def get_order_by_columns(self, order_by_list: list[str]) -> list:
    if len(order_by_list) > MAX_SORT_PARAMS:
        raise HTTPException(
            400,
            f"Ordering with more than {MAX_SORT_PARAMS} parameters is not allowed"
        )
```

3. Use explicit pagination parameters:
```python
def list_items(
    offset: int = 0,
    limit: int = 50,  # Make limits configurable
) -> Response:
    pass
```

This standardization improves API usability, reduces code duplication, and makes the API behavior more predictable for clients.