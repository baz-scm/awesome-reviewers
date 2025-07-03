---
title: Validate inputs explicitly
description: Always validate input parameters and respond with appropriate HTTP status
  codes when invalid values are detected, even when inputs appear controlled by your
  frontend. Backend validation should explicitly check for invalid or unexpected values
  (like "NaN" or values outside an allowed set) and raise appropriate exceptions with
  clear error messages.
repository: kubeflow/kubeflow
label: Error Handling
language: Python
comments_count: 2
repository_stars: 15064
---

Always validate input parameters and respond with appropriate HTTP status codes when invalid values are detected, even when inputs appear controlled by your frontend. Backend validation should explicitly check for invalid or unexpected values (like "NaN" or values outside an allowed set) and raise appropriate exceptions with clear error messages.

Example:
```python
def set_server_type(notebook, body, defaults):
    notebook_annotations = notebook["metadata"]["annotations"]
    server_type = get_form_value(body, defaults, "serverType")
    
    # Validate server type is one of the allowed values
    allowed_types = ["jupyter", "rstudio", "vscode", None]
    if server_type not in allowed_types:
        raise werkzeug.exceptions.BadRequest(
            f"Invalid server type: {server_type}. Must be one of: {allowed_types}")
    
    notebook_annotations["notebooks.kubeflow.org/server-type"] = server_type
```

This practice ensures your API is robust against malformed inputs regardless of their source, provides clear error messages for debugging, and maintains a clean separation of concerns between frontend and backend validation.
