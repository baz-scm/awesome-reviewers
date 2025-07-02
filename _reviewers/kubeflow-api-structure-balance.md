---
title: API structure balance
description: Maintain a clear separation between resource-specific API handlers and
  common utilities. Resource-specific handlers should remain in their dedicated modules
  to reduce dependencies, while common functionality should be extracted into shared
  helpers for consistency.
repository: kubeflow/kubeflow
label: API
language: Python
comments_count: 2
repository_stars: 15064
---

Maintain a clear separation between resource-specific API handlers and common utilities. Resource-specific handlers should remain in their dedicated modules to reduce dependencies, while common functionality should be extracted into shared helpers for consistency.

Example:
```python
# GOOD: Common helper function in a shared utility file
# components/crud-web-apps/common/backend/kubeflow/kubeflow/crud_backend/helpers.py
def get_age(k8s_object):
    """Return age information in a standardized format for any k8s object."""
    creation_time = dt.datetime.strptime(
        k8s_object["metadata"]["creationTimestamp"], "%Y-%m-%dT%H:%M:%SZ")
    uptime = dt.datetime.now() - creation_time
    return {
        "uptime": str(uptime).split('.')[0],  # Remove microseconds
        "timestamp": creation_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

# GOOD: Resource-specific handlers in dedicated modules
# components/model-web-app/backend/app/routes/inference_service.py
def list_inference_services(namespace):
    """Handler specific to InferenceService resources."""
    # Implementation specific to this resource type
```

This approach prevents common code from accumulating resource-specific dependencies while still promoting reuse of utility functions that apply across multiple API endpoints. When designing APIs, always evaluate whether functionality belongs in shared utilities or should remain in resource-specific implementations.


[
  {
    "discussion_id": "1135817898",
    "pr_number": 7019,
    "pr_file": "components/crud-web-apps/common/backend/kubeflow/kubeflow/crud_backend/api/isvc.py",
    "created_at": "2023-03-14T16:16:13+00:00",
    "commented_code": "from . import utils, events\n\n\ndef list_inference_service_events(name, namespace):",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1135817898",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7019,
        "pr_file": "components/crud-web-apps/common/backend/kubeflow/kubeflow/crud_backend/api/isvc.py",
        "discussion_id": "1135817898",
        "commented_code": "@@ -0,0 +1,8 @@\n+from . import utils, events\n+\n+\n+def list_inference_service_events(name, namespace):",
        "comment_created_at": "2023-03-14T16:16:13+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "I'd propose to avoid introducing a handler for the InferenceServices in the common backend code.\r\n\r\nThis would mean we'd need to add more handlers for list/delete/get/logs as well, which as a result will make the MWA depend even more in this common code. I'd propose to instead keep on using the `custom_resource.py` file's handlers for the ISVC logic in the MWA",
        "pr_file_module": null
      },
      {
        "comment_id": "1136863197",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7019,
        "pr_file": "components/crud-web-apps/common/backend/kubeflow/kubeflow/crud_backend/api/isvc.py",
        "discussion_id": "1135817898",
        "commented_code": "@@ -0,0 +1,8 @@\n+from . import utils, events\n+\n+\n+def list_inference_service_events(name, namespace):",
        "comment_created_at": "2023-03-15T10:48:54+00:00",
        "comment_author": "elenzio9",
        "comment_body": "ACK! I've just removed that part and will add the changes to the follow-up PR, which will introduce the `EVENTS` tab, as they'll relate to the MWA backend code.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "467145237",
    "pr_number": 5180,
    "pr_file": "components/crud-web-apps/tensorboards/backend/app/utils.py",
    "created_at": "2020-08-07T16:30:12+00:00",
    "commented_code": "from kubeflow.kubeflow.crud_backend import helpers\n\n\ndef parse_tensorboard(tensorboard):\n    \"\"\"\n    Process the Tensorboard object and format it as the UI expects it.\n    \"\"\"\n\n    parsed_tensorboard = {\n        \"name\": tensorboard['metadata']['name'],\n        \"namespace\": tensorboard['metadata']['namespace'],\n        \"logspath\": tensorboard['spec']['logspath'],\n        \"age\": {",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "467145237",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5180,
        "pr_file": "components/crud-web-apps/tensorboards/backend/app/utils.py",
        "discussion_id": "467145237",
        "commented_code": "@@ -0,0 +1,39 @@\n+from kubeflow.kubeflow.crud_backend import helpers\n+\n+\n+def parse_tensorboard(tensorboard):\n+    \"\"\"\n+    Process the Tensorboard object and format it as the UI expects it.\n+    \"\"\"\n+\n+    parsed_tensorboard = {\n+        \"name\": tensorboard['metadata']['name'],\n+        \"namespace\": tensorboard['metadata']['namespace'],\n+        \"logspath\": tensorboard['spec']['logspath'],\n+        \"age\": {",
        "comment_created_at": "2020-08-07T16:30:12+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "Could you add a `get_age(k8s_object)` in our common [helpers.py](https://github.com/kubeflow/kubeflow/blob/e99b5e18697a15088abea12543bd4e3f180ff984/components/crud-web-apps/common/backend/kubeflow/kubeflow/crud_backend/helpers.py) file that would return a dictionary with the `uptime` and `timestamp` values? Since other web apps will want to use this convention, for returning age information to their frontends, it would be a good idea to add this logic into a common place.\r\n\r\nFor now it could only work with dict objects, like CRs, and later one we could extend it to work with class objects as well, such as PVCs for example.",
        "pr_file_module": null
      },
      {
        "comment_id": "467804614",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5180,
        "pr_file": "components/crud-web-apps/tensorboards/backend/app/utils.py",
        "discussion_id": "467145237",
        "commented_code": "@@ -0,0 +1,39 @@\n+from kubeflow.kubeflow.crud_backend import helpers\n+\n+\n+def parse_tensorboard(tensorboard):\n+    \"\"\"\n+    Process the Tensorboard object and format it as the UI expects it.\n+    \"\"\"\n+\n+    parsed_tensorboard = {\n+        \"name\": tensorboard['metadata']['name'],\n+        \"namespace\": tensorboard['metadata']['namespace'],\n+        \"logspath\": tensorboard['spec']['logspath'],\n+        \"age\": {",
        "comment_created_at": "2020-08-10T10:06:02+00:00",
        "comment_author": "kandrio",
        "comment_body": "Thanks for the comment. I totally agree, so I just added a new commit that adds `get_age(k8s_object)` to the common code.",
        "pr_file_module": null
      }
    ]
  }
]
