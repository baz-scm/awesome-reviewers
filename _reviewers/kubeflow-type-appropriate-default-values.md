---
title: Type-appropriate default values
description: Initialize variables with type-appropriate default values to prevent
  type errors and null reference exceptions during operations. When a variable is
  expected to hold a collection type (list, dictionary, set), use the corresponding
  empty collection (`[]`, `{}`, `set()`) rather than other falsy values like `None`
  or empty strings.
repository: kubeflow/kubeflow
label: Null Handling
language: Python
comments_count: 2
repository_stars: 15064
---

Initialize variables with type-appropriate default values to prevent type errors and null reference exceptions during operations. When a variable is expected to hold a collection type (list, dictionary, set), use the corresponding empty collection (`[]`, `{}`, `set()`) rather than other falsy values like `None` or empty strings.

For example, instead of:
```python
conditions = notebook.get("status", {}).get("conditions", "")
# Using "" as default for a variable that should be a list is problematic
if some_condition:
    conditions.append(new_item)  # This will fail if conditions is ""
```

Use type-appropriate defaults:
```python
conditions = notebook.get("status", {}).get("conditions", [])
# Using [] as default ensures the variable is always a list
if some_condition:
    conditions.append(new_item)  # This will work regardless
```

For complex data structures like dictionaries passed as parameters, consider adding type hints or documentation that clearly defines the expected structure, including which fields are optional vs. required. This helps prevent null reference errors when accessing dictionary keys.


[
  {
    "discussion_id": "1146054284",
    "pr_number": 6952,
    "pr_file": "components/crud-web-apps/jupyter/backend/apps/common/status.py",
    "created_at": "2023-03-23T11:38:26+00:00",
    "commented_code": "def process_status(notebook):\n    \"\"\"\n    Return status and reason. Status may be [running|waiting|warning|error]\n    Return status and reason. Status may be [running|waiting|warning]\n    \"\"\"\n    # Check if the Notebook is stopped\n    readyReplicas = notebook.get(\"status\", {}).get(\"readyReplicas\", 0)\n    metadata = notebook.get(\"metadata\", {})\n    annotations = metadata.get(\"annotations\", {})\n\n    if STOP_ANNOTATION in annotations:\n        if readyReplicas == 0:\n            return status.create_status(\n                status.STATUS_PHASE.STOPPED,\n                \"No Pods are currently running for this Notebook Server.\",\n            )\n        else:\n            return status.create_status(\n                status.STATUS_PHASE.TERMINATING, \"Notebook Server is stopping.\"\n            )\n    creationTimestamp = notebook[\"metadata\"][\"creationTimestamp\"]\n\n    # If the Notebook is being deleted, the status will be waiting\n    if \"deletionTimestamp\" in metadata:\n        return status.create_status(\n            status.STATUS_PHASE.TERMINATING, \"Deleting this notebook server\"\n        )\n\n    # Check the status\n    state = notebook.get(\"status\", {}).get(\"containerState\", \"\")\n\n    # Use conditions on the Jupyter notebook (i.e., s) to determine overall\n    # status. If no container state is available, we try to extract information\n    # about why the notebook is not starting from the notebook's events\n    # (see find_error_event)\n    if readyReplicas == 1:\n        return status.create_status(status.STATUS_PHASE.READY, \"Running\")\n\n    if \"waiting\" in state:\n        return status.create_status(\n            status.STATUS_PHASE.WAITING, state[\"waiting\"][\"reason\"]\n        )\n\n    # Provide the user with detailed information (if any) about\n    # why the notebook is not starting\n    notebook_events = get_notebook_events(notebook)\n    status_val, reason = status.STATUS_PHASE.WAITING, \"Scheduling the Pod\"\n    status_event, reason_event = find_error_event(notebook_events)\n    if status_event is not None:\n        status_val, reason = status_event, reason_event\n\n    return status.create_status(status_val, reason)\n    # Convert a date string of a format to datetime object\n    nb_creation_time = dt.datetime.strptime(\n        creationTimestamp, \"%Y-%m-%dT%H:%M:%SZ\")\n    current_time = dt.datetime.utcnow().replace(microsecond=0)\n    delta = (current_time - nb_creation_time)\n\n    while delta.total_seconds() <= 10:\n        status_val, reason = status.STATUS_PHASE.WAITING, \"Waiting for StatefulSet to create the underlying Pod.\"\n\n        # Check if the Notebook is stopped or deleted\n        status_phase, status_message = check_stopped_deleted_nb(notebook)\n        if status_phase is not None:\n            status_val, reason = status_phase, status_message\n\n        return status.create_status(status_val, reason)\n    else:\n        # Check if the Notebook is stopped or deleted\n        status_phase, status_message = check_stopped_deleted_nb(notebook)\n        if status_phase is not None:\n            status_val, reason = status_phase, status_message\n            return status.create_status(status_val, reason)\n\n        # If the Notebook is running, the status will be ready\n        if readyReplicas == 1:\n            return status.create_status(status.STATUS_PHASE.READY, \"Running\")\n\n        # Otherwise, first check .status.containerState to determine the status\n        # reason and message to determine the status\n        containerState = notebook.get(\"status\", {}).get(\"containerState\", \"\")\n\n        if \"waiting\" in containerState:\n            if containerState[\"waiting\"][\"reason\"] == 'PodInitializing':\n                return status.create_status(\n                    status.STATUS_PHASE.WAITING, containerState[\"waiting\"][\"reason\"]\n                )\n            else:\n                return status.create_status(\n                    status.STATUS_PHASE.WARNING, containerState[\"waiting\"][\"reason\"] +\n                    ': ' + containerState[\"waiting\"][\"message\"]\n                )\n\n        # If no containerState is available, check .status.conditions, since they have\n        # a reason and a message to determine the status\n        conditions = notebook.get(\"status\", {}).get(\"conditions\", \"\")",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1146054284",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6952,
        "pr_file": "components/crud-web-apps/jupyter/backend/apps/common/status.py",
        "discussion_id": "1146054284",
        "commented_code": "@@ -8,54 +8,75 @@\n \n def process_status(notebook):\n     \"\"\"\n-    Return status and reason. Status may be [running|waiting|warning|error]\n+    Return status and reason. Status may be [running|waiting|warning]\n     \"\"\"\n-    # Check if the Notebook is stopped\n     readyReplicas = notebook.get(\"status\", {}).get(\"readyReplicas\", 0)\n-    metadata = notebook.get(\"metadata\", {})\n-    annotations = metadata.get(\"annotations\", {})\n-\n-    if STOP_ANNOTATION in annotations:\n-        if readyReplicas == 0:\n-            return status.create_status(\n-                status.STATUS_PHASE.STOPPED,\n-                \"No Pods are currently running for this Notebook Server.\",\n-            )\n-        else:\n-            return status.create_status(\n-                status.STATUS_PHASE.TERMINATING, \"Notebook Server is stopping.\"\n-            )\n+    creationTimestamp = notebook[\"metadata\"][\"creationTimestamp\"]\n \n-    # If the Notebook is being deleted, the status will be waiting\n-    if \"deletionTimestamp\" in metadata:\n-        return status.create_status(\n-            status.STATUS_PHASE.TERMINATING, \"Deleting this notebook server\"\n-        )\n-\n-    # Check the status\n-    state = notebook.get(\"status\", {}).get(\"containerState\", \"\")\n-\n-    # Use conditions on the Jupyter notebook (i.e., s) to determine overall\n-    # status. If no container state is available, we try to extract information\n-    # about why the notebook is not starting from the notebook's events\n-    # (see find_error_event)\n-    if readyReplicas == 1:\n-        return status.create_status(status.STATUS_PHASE.READY, \"Running\")\n-\n-    if \"waiting\" in state:\n-        return status.create_status(\n-            status.STATUS_PHASE.WAITING, state[\"waiting\"][\"reason\"]\n-        )\n-\n-    # Provide the user with detailed information (if any) about\n-    # why the notebook is not starting\n-    notebook_events = get_notebook_events(notebook)\n-    status_val, reason = status.STATUS_PHASE.WAITING, \"Scheduling the Pod\"\n-    status_event, reason_event = find_error_event(notebook_events)\n-    if status_event is not None:\n-        status_val, reason = status_event, reason_event\n-\n-    return status.create_status(status_val, reason)\n+    # Convert a date string of a format to datetime object\n+    nb_creation_time = dt.datetime.strptime(\n+        creationTimestamp, \"%Y-%m-%dT%H:%M:%SZ\")\n+    current_time = dt.datetime.utcnow().replace(microsecond=0)\n+    delta = (current_time - nb_creation_time)\n+\n+    while delta.total_seconds() <= 10:\n+        status_val, reason = status.STATUS_PHASE.WAITING, \"Waiting for StatefulSet to create the underlying Pod.\"\n+\n+        # Check if the Notebook is stopped or deleted\n+        status_phase, status_message = check_stopped_deleted_nb(notebook)\n+        if status_phase is not None:\n+            status_val, reason = status_phase, status_message\n+\n+        return status.create_status(status_val, reason)\n+    else:\n+        # Check if the Notebook is stopped or deleted\n+        status_phase, status_message = check_stopped_deleted_nb(notebook)\n+        if status_phase is not None:\n+            status_val, reason = status_phase, status_message\n+            return status.create_status(status_val, reason)\n+\n+        # If the Notebook is running, the status will be ready\n+        if readyReplicas == 1:\n+            return status.create_status(status.STATUS_PHASE.READY, \"Running\")\n+\n+        # Otherwise, first check .status.containerState to determine the status\n+        # reason and message to determine the status\n+        containerState = notebook.get(\"status\", {}).get(\"containerState\", \"\")\n+\n+        if \"waiting\" in containerState:\n+            if containerState[\"waiting\"][\"reason\"] == 'PodInitializing':\n+                return status.create_status(\n+                    status.STATUS_PHASE.WAITING, containerState[\"waiting\"][\"reason\"]\n+                )\n+            else:\n+                return status.create_status(\n+                    status.STATUS_PHASE.WARNING, containerState[\"waiting\"][\"reason\"] +\n+                    ': ' + containerState[\"waiting\"][\"message\"]\n+                )\n+\n+        # If no containerState is available, check .status.conditions, since they have\n+        # a reason and a message to determine the status\n+        conditions = notebook.get(\"status\", {}).get(\"conditions\", \"\")",
        "comment_created_at": "2023-03-23T11:38:26+00:00",
        "comment_author": "kimwnasptd",
        "comment_body": "In this case the default value for the conditions should be a `[]`, instead of `\"\"` since this var is a list",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "265194749",
    "pr_number": 2679,
    "pr_file": "components/jupyter-web-app/default/kubeflow/jupyter/server.py",
    "created_at": "2019-03-13T15:43:06+00:00",
    "commented_code": "return err\n\n\ndef create_workspace_pvc(body):\n  \"\"\"If the type is New, then create a new PVC, else use an existing one\"\"\"\n  if body[\"ws_type\"] == \"New\":\n    pvc = client.V1PersistentVolumeClaim(\n        metadata=client.V1ObjectMeta(\n            name=body['ws_name'],\n            namespace=body['ns']\n        ),\n        spec=client.V1PersistentVolumeClaimSpec(\n            access_modes=[body['ws_access_modes']],\n            resources=client.V1ResourceRequirements(\n                requests={\n                    'storage': body['ws_size'] + 'Gi'\n                }\n            )\n        )\n    )\n\n    create_pvc(pvc)\n\n  return\n\n\ndef create_datavol_pvc(body, i):",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "265194749",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 2679,
        "pr_file": "components/jupyter-web-app/default/kubeflow/jupyter/server.py",
        "discussion_id": "265194749",
        "commented_code": "@@ -26,10 +30,79 @@ def parse_error(e):\n   return err\n \n \n+def create_workspace_pvc(body):\n+  \"\"\"If the type is New, then create a new PVC, else use an existing one\"\"\"\n+  if body[\"ws_type\"] == \"New\":\n+    pvc = client.V1PersistentVolumeClaim(\n+        metadata=client.V1ObjectMeta(\n+            name=body['ws_name'],\n+            namespace=body['ns']\n+        ),\n+        spec=client.V1PersistentVolumeClaimSpec(\n+            access_modes=[body['ws_access_modes']],\n+            resources=client.V1ResourceRequirements(\n+                requests={\n+                    'storage': body['ws_size'] + 'Gi'\n+                }\n+            )\n+        )\n+    )\n+\n+    create_pvc(pvc)\n+\n+  return\n+\n+\n+def create_datavol_pvc(body, i):",
        "comment_created_at": "2019-03-13T15:43:06+00:00",
        "comment_author": "prodonjs",
        "comment_body": "Ideally I think there would be some kind of definition for the shape of the body dict being passed in, but since I have almost no context of looking at this I'm not going to be picky.",
        "pr_file_module": null
      }
    ]
  }
]
