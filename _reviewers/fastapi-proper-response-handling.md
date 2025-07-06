---
title: Proper response handling
description: 'When designing APIs, ensure responses adhere to HTTP semantics by:


  1. Using semantic status code constants instead of magic numbers

  ```python

  # Bad

  raise HTTPException(status_code=400, detail="Inactive user")'
repository: fastapi/fastapi
label: API
language: Python
comments_count: 3
repository_stars: 86871
---

When designing APIs, ensure responses adhere to HTTP semantics by:

1. Using semantic status code constants instead of magic numbers
```python
# Bad
raise HTTPException(status_code=400, detail="Inactive user")

# Good
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
)
```

2. Choosing status codes based on their semantic meaning:
   - 400: Client error (malformed request)
   - 403: Authentication succeeded but authorization failed
   - 204: Success with no content

3. Matching response types to HTTP methods:
```python
# Bad for HEAD requests
def head_item(item_id: str):
    return JSONResponse(None, headers={"x-item-id": item_id})

# Good for HEAD requests
def head_item(item_id: str):
    return Response(headers={"x-item-id": item_id})
```

4. Testing responses thoroughly, including both status code and content:
```python
# More complete test
def test_no_content():
    response = client.get("/no-content")
    assert response.status_code == http.HTTPStatus.NO_CONTENT
    assert not response.content
```

Following these practices improves API reliability, interoperability, and compliance with HTTP standards.