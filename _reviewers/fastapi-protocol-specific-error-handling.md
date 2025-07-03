---
title: Protocol-specific error handling
description: Handle errors and responses appropriately based on the network protocol
  being used. Different protocols have different mechanisms for error reporting and
  communication patterns.
repository: fastapi/fastapi
label: Networking
language: Markdown
comments_count: 5
repository_stars: 86871
---

Handle errors and responses appropriately based on the network protocol being used. Different protocols have different mechanisms for error reporting and communication patterns.

For HTTP endpoints:
- Use appropriate HTTP status codes to communicate the nature of the response
- Return 2xx codes for successful operations, 4xx for client errors, 5xx for server errors
- Include descriptive error messages in the response body for client errors
- Configure CORS headers correctly, especially when using credentials:
  ```python
  # When allow_credentials is True, avoid wildcards
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["https://specific-origin.com"],  # Not ['*']
      allow_methods=["GET", "POST"],  # Not ['*']
      allow_headers=["X-Custom-Header"],  # Not ['*']
      allow_credentials=True
  )
  ```

For WebSockets:
- Don't raise HTTP exceptions in WebSocket handlers
- Close the connection directly with an appropriate code when errors occur:
  ```python
  @app.websocket("/ws")
  async def websocket_endpoint(websocket: WebSocket):
      await websocket.accept()
      try:
          while True:
              data = await websocket.receive_text()
              # Process data
              if error_condition:
                  # Don't use HTTPException here
                  await websocket.close(code=1008)  # Policy violation
                  return
      except Exception:
          await websocket.close(code=1011)  # Internal error
  ```

For custom headers:
- Use 'X-' prefix for custom headers in server-to-server communication
- When browsers need to access custom headers in cross-origin requests, add them to your CORS configuration with the `expose_headers` parameter