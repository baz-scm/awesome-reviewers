---
title: Document all responses
description: 'When designing APIs, thoroughly document all possible responses your
  endpoints can return, not just the "happy path" success cases. Include documentation
  for:'
repository: fastapi/fastapi
label: API
language: Markdown
comments_count: 8
repository_stars: 86871
---

When designing APIs, thoroughly document all possible responses your endpoints can return, not just the "happy path" success cases. Include documentation for:

1. Success responses with different status codes (e.g., 200 OK, 201 Created)
2. Error responses with appropriate status codes (400-range for client errors, 500-range for server errors)
3. Response structure for each status code
4. Conditions that trigger each response type

For example, in FastAPI you can document multiple response scenarios using the `responses` parameter:

```python
@app.get(
    "/items/{item_id}",
    responses={
        200: {
            "description": "Successful Response",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Item"}}}
        },
        404: {
            "description": "Item Not Found",
            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Message"}}}
        }
    }
)
def read_item(item_id: int):
    if item_id not in items:
        return JSONResponse(
            status_code=404,
            content={"message": "Item not found"}
        )
    return items[item_id]
```

By documenting all possible responses, you provide API consumers with the information they need to properly handle all scenarios, improving the robustness of applications built on your API and reducing integration time.