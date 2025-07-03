---
title: Prioritize readability over brevity
description: 'When writing code, favor readability and maintainability over clever
  or compact solutions. Break down complex logic into smaller, well-named functions
  with clear purposes rather than embedding all logic in a single function. '
repository: kubeflow/kubeflow
label: Code Style
language: Python
comments_count: 4
repository_stars: 15064
---

When writing code, favor readability and maintainability over clever or compact solutions. Break down complex logic into smaller, well-named functions with clear purposes rather than embedding all logic in a single function. 

Follow these specific practices:

1. Extract related logic into separate, focused functions even when used only once:
```python
# Instead of this:
def patch_notebook(namespace, notebook):
    # ... some code ...
    if STOP_ATTR in request_body:
        # Many lines of complex start/stop logic here
    # ... more code ...

# Prefer this:
def patch_notebook(namespace, notebook):
    # ... some code ...
    if STOP_ATTR in request_body:
        start_stop_notebook(namespace, notebook, request_body)
    # ... more code ...

def start_stop_notebook(namespace, notebook, request_body):
    # Start/stop logic extracted here
```

2. Avoid complex one-liners that span multiple lines. Instead of:
```python
resp = requests.request("GET", url, verify=False) if use_basic_auth else requests.request("GET", url, headers={"Authorization": "Bearer {}".format(token)}, verify=False)
```

Prefer:
```python
if use_basic_auth:
    resp = requests.request("GET", url, verify=False)
else:
    resp = requests.request(
        "GET", 
        url, 
        headers={"Authorization": "Bearer {}".format(token)},
        verify=False
    )
```

3. For long lines, don't ignore linter warnings (like E501). Put arguments on separate lines:
```python
# Instead of:
@bp.route("/api/namespaces/<namespace>/tensorboards/<tensorboard>", methods=["DELETE"])  # noqa E501

# Prefer:
@bp.route(
    "/api/namespaces/<namespace>/tensorboards/<tensorboard>", 
    methods=["DELETE"]
)
```

This approach makes code easier to read, maintain, and debug, improving the overall quality of the codebase.
