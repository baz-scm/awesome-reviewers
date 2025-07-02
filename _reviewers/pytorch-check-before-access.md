---
title: Check before access
description: Always check for null/None values and verify attribute/key existence
  before accessing them. This prevents runtime errors like AttributeError or KeyError
  that occur when accessing attributes on None or missing dictionary keys.
repository: pytorch/pytorch
label: Null Handling
language: Python
comments_count: 7
repository_stars: 91169
---

Always check for null/None values and verify attribute/key existence before accessing them. This prevents runtime errors like AttributeError or KeyError that occur when accessing attributes on None or missing dictionary keys.

When accessing attributes:
```python
# Bad: May cause AttributeError if current_accelerator() returns None
device_type = torch.accelerator.current_accelerator().type

# Good: Check before access
accelerator = torch.accelerator.current_accelerator()
if accelerator is not None:
    device_type = accelerator.type
else:
    device_type = "cpu"  # Default fallback

# Bad: May cause AttributeError if func doesn't have tags attribute
if torch.Tag.inplace_view in func.tags:
    # ...

# Good: Check attribute existence first
if hasattr(func, "tags") and torch.Tag.inplace_view in func.tags:
    # ...
```

When accessing dictionary keys:
```python
# Bad: May raise KeyError if key doesn't exist
lst.append(f'* {obj["DeviceName"]}')

# Good: Use .get() with a default value
lst.append(f'* {obj.get("DeviceName", "N/A")}')

# Bad: May fail if device_list is missing or not a list
if type(obj["device_list"]) is list:
    # ...

# Good: Check existence and type safely
device_list = obj.get("device_list", [])
if isinstance(device_list, list) and device_list:
    # ...
```

When checking types:
```python
# Bad: May fail if storage_writer is None
if isinstance(storage_writer, AsyncStager):
    # ...

# Good: Check for None first
if storage_writer is not None and isinstance(storage_writer, AsyncStager):
    # ...
```

This defensive programming approach reduces unexpected crashes and improves code robustness.


[
  {
    "discussion_id": "2166162800",
    "pr_number": 156796,
    "pr_file": "test/distributed/checkpoint/test_state_dict.py",
    "created_at": "2025-06-25T08:43:36+00:00",
    "commented_code": "from torch.utils._pytree import tree_all, tree_all_only\n\n\ndevice_type = torch.accelerator.current_accelerator().type",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2166162800",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156796,
        "pr_file": "test/distributed/checkpoint/test_state_dict.py",
        "discussion_id": "2166162800",
        "commented_code": "@@ -62,6 +62,9 @@\n from torch.utils._pytree import tree_all, tree_all_only\n \n \n+device_type = torch.accelerator.current_accelerator().type",
        "comment_created_at": "2025-06-25T08:43:36+00:00",
        "comment_author": "zeshengzong",
        "comment_body": "Hi, `torch.accelerator.current_accelerator()` will return `None` when accelerator not detected, is there a check before running these tests? Thanks!",
        "pr_file_module": null
      },
      {
        "comment_id": "2167354355",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156796,
        "pr_file": "test/distributed/checkpoint/test_state_dict.py",
        "discussion_id": "2166162800",
        "commented_code": "@@ -62,6 +62,9 @@\n from torch.utils._pytree import tree_all, tree_all_only\n \n \n+device_type = torch.accelerator.current_accelerator().type",
        "comment_created_at": "2025-06-25T18:31:47+00:00",
        "comment_author": "harikodali",
        "comment_body": "thanks for spotting, it's an oversight, changed it to use get_devtype from common_fsdp instead",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2170357623",
    "pr_number": 156689,
    "pr_file": "torch/_subclasses/fake_tensor.py",
    "created_at": "2025-06-27T00:34:32+00:00",
    "commented_code": "nonlocal flat_arg_fake_tensors\n            if not self.is_our_fake(x):\n                if torch.Tag.inplace_view in func.tags:\n                if hasattr(func, \"tags\") and torch.Tag.inplace_view in func.tags:",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2170357623",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156689,
        "pr_file": "torch/_subclasses/fake_tensor.py",
        "discussion_id": "2170357623",
        "commented_code": "@@ -2774,7 +2774,7 @@ def validate(x: T) -> Union[T, FakeTensor]:\n \n             nonlocal flat_arg_fake_tensors\n             if not self.is_our_fake(x):\n-                if torch.Tag.inplace_view in func.tags:\n+                if hasattr(func, \"tags\") and torch.Tag.inplace_view in func.tags:",
        "comment_created_at": "2025-06-27T00:34:32+00:00",
        "comment_author": "leslie-fang-intel",
        "comment_body": "The changes in this PR looks good to me. But\r\nwhen auditing the code, I noticed many instances where `func.tags` is used without checking whether `func` actually has a `tags` attribute. Do we need to review other parts of the code for similar issues or should we add the `tags` attribute to `HigherOrderOperator`? also cc @bdhirsh ",
        "pr_file_module": null
      },
      {
        "comment_id": "2178804285",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156689,
        "pr_file": "torch/_subclasses/fake_tensor.py",
        "discussion_id": "2170357623",
        "commented_code": "@@ -2774,7 +2774,7 @@ def validate(x: T) -> Union[T, FakeTensor]:\n \n             nonlocal flat_arg_fake_tensors\n             if not self.is_our_fake(x):\n-                if torch.Tag.inplace_view in func.tags:\n+                if hasattr(func, \"tags\") and torch.Tag.inplace_view in func.tags:",
        "comment_created_at": "2025-07-02T01:27:13+00:00",
        "comment_author": "Valentine233",
        "comment_body": "Thanks, good point! We can discuss more in this thread, and do the follow-up in the future.\r\nBut I suppose we can firstly land this PR, as urgently required in v2.8 release. ",
        "pr_file_module": null
      },
      {
        "comment_id": "2179394831",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156689,
        "pr_file": "torch/_subclasses/fake_tensor.py",
        "discussion_id": "2170357623",
        "commented_code": "@@ -2774,7 +2774,7 @@ def validate(x: T) -> Union[T, FakeTensor]:\n \n             nonlocal flat_arg_fake_tensors\n             if not self.is_our_fake(x):\n-                if torch.Tag.inplace_view in func.tags:\n+                if hasattr(func, \"tags\") and torch.Tag.inplace_view in func.tags:",
        "comment_created_at": "2025-07-02T08:01:11+00:00",
        "comment_author": "leslie-fang-intel",
        "comment_body": "> Thanks, good point! We can discuss more in this thread, and do the follow-up in the future. But I suppose we can firstly land this PR, as urgently required in v2.8 release.\r\n\r\nLooks good to me given the changes in this PR should be no side effect. Will you further work on for a formal solution?",
        "pr_file_module": null
      },
      {
        "comment_id": "2179405142",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156689,
        "pr_file": "torch/_subclasses/fake_tensor.py",
        "discussion_id": "2170357623",
        "commented_code": "@@ -2774,7 +2774,7 @@ def validate(x: T) -> Union[T, FakeTensor]:\n \n             nonlocal flat_arg_fake_tensors\n             if not self.is_our_fake(x):\n-                if torch.Tag.inplace_view in func.tags:\n+                if hasattr(func, \"tags\") and torch.Tag.inplace_view in func.tags:",
        "comment_created_at": "2025-07-02T08:06:24+00:00",
        "comment_author": "Valentine233",
        "comment_body": "Maybe needs some inputs from @bdhirsh about why `HigherOrderOperator` does not have `tags` attribute. Is this part of design or should we add `tags` for `HigherOrderOperator`?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2176304626",
    "pr_number": 157317,
    "pr_file": "torch/distributed/tensor/examples/comm_mode_features_example.py",
    "created_at": "2025-07-01T02:44:09+00:00",
    "commented_code": null,
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2176304626",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 157317,
        "pr_file": "torch/distributed/tensor/examples/comm_mode_features_example.py",
        "discussion_id": "2176304626",
        "commented_code": null,
        "comment_created_at": "2025-07-01T02:44:09+00:00",
        "comment_author": "githubsgi",
        "comment_body": "This would fail as follows. \r\n\r\n```\r\n  Error (MYPY) [union-attr]\r\n    Item \"None\" of \"device | None\" has no attribute \"type\"\r\n\r\n         28  |\r\n         29  |def get_device_type() -> str:\r\n         30  |    return (\r\n    >>>  31  |        torch.accelerator.current_accelerator().type\r\n         32  |        if torch.accelerator.device_count() >= 4\r\n         33  |        else \"cpu\"\r\n         34  |    )\r\n\r\n+ echo ''\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2176308770",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 157317,
        "pr_file": "torch/distributed/tensor/examples/comm_mode_features_example.py",
        "discussion_id": "2176304626",
        "commented_code": null,
        "comment_created_at": "2025-07-01T02:50:01+00:00",
        "comment_author": "EikanWang",
        "comment_body": "`current_accelerator` could return `None`.",
        "pr_file_module": null
      },
      {
        "comment_id": "2176308958",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 157317,
        "pr_file": "torch/distributed/tensor/examples/comm_mode_features_example.py",
        "discussion_id": "2176304626",
        "commented_code": null,
        "comment_created_at": "2025-07-01T02:50:21+00:00",
        "comment_author": "EikanWang",
        "comment_body": "The code needs to be polished a little bit.",
        "pr_file_module": null
      },
      {
        "comment_id": "2176368205",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 157317,
        "pr_file": "torch/distributed/tensor/examples/comm_mode_features_example.py",
        "discussion_id": "2176304626",
        "commented_code": null,
        "comment_created_at": "2025-07-01T04:13:22+00:00",
        "comment_author": "guangyey",
        "comment_body": "If `torch.accelerator.device_count() >= 4` is `True`, `torch.accelerator.current_accelerator()` must not return `None`\r\nI think it is OK to refine it or ignore the linter `# type: ignore[union-attr]`",
        "pr_file_module": null
      },
      {
        "comment_id": "2176547066",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 157317,
        "pr_file": "torch/distributed/tensor/examples/comm_mode_features_example.py",
        "discussion_id": "2176304626",
        "commented_code": null,
        "comment_created_at": "2025-07-01T06:35:54+00:00",
        "comment_author": "githubsgi",
        "comment_body": "@guangyey , I think it is better  not to change the original  logic.  ",
        "pr_file_module": null
      },
      {
        "comment_id": "2176553104",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 157317,
        "pr_file": "torch/distributed/tensor/examples/comm_mode_features_example.py",
        "discussion_id": "2176304626",
        "commented_code": null,
        "comment_created_at": "2025-07-01T06:39:11+00:00",
        "comment_author": "guangyey",
        "comment_body": "Sounds good.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2083884131",
    "pr_number": 153213,
    "pr_file": "torch/distributed/tensor/examples/comm_mode_features_example.py",
    "created_at": "2025-05-12T06:08:05+00:00",
    "commented_code": "def __init__(self, world_size: int, rank: int) -> None:\n        self.world_size = world_size\n        self.rank = rank\n        self.device_type = get_device_type()\n        self.device_type = torch.accelerator.current_accelerator().type",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2083884131",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 153213,
        "pr_file": "torch/distributed/tensor/examples/comm_mode_features_example.py",
        "discussion_id": "2083884131",
        "commented_code": "@@ -49,7 +41,7 @@ class CommDebugModeExample:\n     def __init__(self, world_size: int, rank: int) -> None:\n         self.world_size = world_size\n         self.rank = rank\n-        self.device_type = get_device_type()\n+        self.device_type = torch.accelerator.current_accelerator().type",
        "comment_created_at": "2025-05-12T06:08:05+00:00",
        "comment_author": "EikanWang",
        "comment_body": "`torch.accelerator.current_accelerator()` may return `None`. Pls. handle the `None` case.",
        "pr_file_module": null
      },
      {
        "comment_id": "2083885848",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 153213,
        "pr_file": "torch/distributed/tensor/examples/comm_mode_features_example.py",
        "discussion_id": "2083884131",
        "commented_code": "@@ -49,7 +41,7 @@ class CommDebugModeExample:\n     def __init__(self, world_size: int, rank: int) -> None:\n         self.world_size = world_size\n         self.rank = rank\n-        self.device_type = get_device_type()\n+        self.device_type = torch.accelerator.current_accelerator().type",
        "comment_created_at": "2025-05-12T06:09:57+00:00",
        "comment_author": "EikanWang",
        "comment_body": "`get_device_type` requires the device count to be `>=4`. The current logic missed the check.",
        "pr_file_module": null
      },
      {
        "comment_id": "2083888453",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 153213,
        "pr_file": "torch/distributed/tensor/examples/comm_mode_features_example.py",
        "discussion_id": "2083884131",
        "commented_code": "@@ -49,7 +41,7 @@ class CommDebugModeExample:\n     def __init__(self, world_size: int, rank: int) -> None:\n         self.world_size = world_size\n         self.rank = rank\n-        self.device_type = get_device_type()\n+        self.device_type = torch.accelerator.current_accelerator().type",
        "comment_created_at": "2025-05-12T06:10:42+00:00",
        "comment_author": "EikanWang",
        "comment_body": "`torch.accelerator.current_accelerator()` does not contain `cpu` devices. Pls add the `cpu` support.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2023983308",
    "pr_number": 137846,
    "pr_file": "torch/utils/collect_env.py",
    "created_at": "2025-04-02T02:46:51+00:00",
    "commented_code": "return smi\n\n\ndef get_intel_gpu_onboard(run_lambda):\n    lst = []\n    platform = get_platform()\n    if platform == \"linux\":\n        txt = run_and_read_all(run_lambda, \"xpu-smi discovery -j\")\n        if txt:\n            try:\n                obj = json.loads(txt)\n                if type(obj[\"device_list\"]) is list:\n                    for o in obj[\"device_list\"]:\n                        lst.append(f'* {o[\"device_name\"]}')",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2023983308",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 137846,
        "pr_file": "torch/utils/collect_env.py",
        "discussion_id": "2023983308",
        "commented_code": "@@ -243,6 +247,56 @@ def get_nvidia_smi():\n     return smi\n \n \n+def get_intel_gpu_onboard(run_lambda):\n+    lst = []\n+    platform = get_platform()\n+    if platform == \"linux\":\n+        txt = run_and_read_all(run_lambda, \"xpu-smi discovery -j\")\n+        if txt:\n+            try:\n+                obj = json.loads(txt)\n+                if type(obj[\"device_list\"]) is list:\n+                    for o in obj[\"device_list\"]:\n+                        lst.append(f'* {o[\"device_name\"]}')",
        "comment_created_at": "2025-04-02T02:46:51+00:00",
        "comment_author": "guangyey",
        "comment_body": "```suggestion\r\n                device_list = obj.get(\"device_list\", [])\r\n                if isinstance(device_list, list) and device_list:\r\n                    lst.extend(f'* {o[\"device_name\"]}' for device in device_list)\r\n                else:\r\n                    lst.append(\"N/A\")\r\n```\r\nAvoid obj[\"device_list\"] is empty and check it before iteration.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2023996133",
    "pr_number": 137846,
    "pr_file": "torch/utils/collect_env.py",
    "created_at": "2025-04-02T02:59:16+00:00",
    "commented_code": "return smi\n\n\ndef get_intel_gpu_onboard(run_lambda):\n    lst = []\n    platform = get_platform()\n    if platform == \"linux\":\n        txt = run_and_read_all(run_lambda, \"xpu-smi discovery -j\")\n        if txt:\n            try:\n                obj = json.loads(txt)\n                if type(obj[\"device_list\"]) is list:\n                    for o in obj[\"device_list\"]:\n                        lst.append(f'* {o[\"device_name\"]}')\n                else:\n                    lst.append(\"N/A\")\n            except (ValueError, TypeError) as e:\n                lst.append(str(e))\n        else:\n            lst.append(\"N/A\")\n    if platform == \"win32\" or platform == \"cygwin\":\n        txt = run_and_read_all(\n            run_lambda,\n            'powershell.exe \"gwmi -Class Win32_PnpSignedDriver | where{$_.DeviceClass -eq \\\\\"DISPLAY\\\\\"\\\n            -and $_.Manufacturer -match \\\\\"Intel\\\\\"} | Select-Object -Property DeviceName | ConvertTo-Json\"',\n        )\n        try:\n            obj = json.loads(txt)\n            if type(obj) is list:\n                for o in obj:\n                    lst.append(f'* {o[\"DeviceName\"]}')\n            else:\n                lst.append(f'* {obj[\"DeviceName\"]}')",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2023996133",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 137846,
        "pr_file": "torch/utils/collect_env.py",
        "discussion_id": "2023996133",
        "commented_code": "@@ -243,6 +247,56 @@ def get_nvidia_smi():\n     return smi\n \n \n+def get_intel_gpu_onboard(run_lambda):\n+    lst = []\n+    platform = get_platform()\n+    if platform == \"linux\":\n+        txt = run_and_read_all(run_lambda, \"xpu-smi discovery -j\")\n+        if txt:\n+            try:\n+                obj = json.loads(txt)\n+                if type(obj[\"device_list\"]) is list:\n+                    for o in obj[\"device_list\"]:\n+                        lst.append(f'* {o[\"device_name\"]}')\n+                else:\n+                    lst.append(\"N/A\")\n+            except (ValueError, TypeError) as e:\n+                lst.append(str(e))\n+        else:\n+            lst.append(\"N/A\")\n+    if platform == \"win32\" or platform == \"cygwin\":\n+        txt = run_and_read_all(\n+            run_lambda,\n+            'powershell.exe \"gwmi -Class Win32_PnpSignedDriver | where{$_.DeviceClass -eq \\\\\"DISPLAY\\\\\"\\\n+            -and $_.Manufacturer -match \\\\\"Intel\\\\\"} | Select-Object -Property DeviceName | ConvertTo-Json\"',\n+        )\n+        try:\n+            obj = json.loads(txt)\n+            if type(obj) is list:\n+                for o in obj:\n+                    lst.append(f'* {o[\"DeviceName\"]}')\n+            else:\n+                lst.append(f'* {obj[\"DeviceName\"]}')",
        "comment_created_at": "2025-04-02T02:59:16+00:00",
        "comment_author": "guangyey",
        "comment_body": "```suggestion\r\n                lst.append(f'* {obj.get(\"DeviceName\", \"N/A\"}')\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2159408147",
    "pr_number": 156207,
    "pr_file": "torch/distributed/checkpoint/state_dict_saver.py",
    "created_at": "2025-06-20T17:16:56+00:00",
    "commented_code": "\"A CPU backend must be enabled for async save; try initializing process group with 'cpu:gloo,cuda:nccl'\"\n        )\n\n    use_default_staging = False\n    if storage_writer is None:\n        use_default_staging = True\n\n    storage_writer = cast(\n        StorageWriter, _storage_setup(storage_writer, checkpoint_id, reader=False)\n    )\n\n    state_dict = _stateful_to_state_dict(state_dict)\n\n    @_dcp_method_logger(log_exceptions=True)\n    def stage_state_dict():\n        if isinstance(storage_writer, AsyncStager):\n            staged_state_dict = storage_writer.stage(state_dict)\n        else:  # provides bwc for storage_writers not implementing AsyncStager\n            staged_state_dict = _create_cpu_state_dict(state_dict)\n            _copy_state_dict(state_dict, staged_state_dict, type_check=False)\n\n        return staged_state_dict\n\n    staged_state_dict = stage_state_dict()\n\n    executor: _AsyncCheckpointExecutor = (\n    def stage_state_dict() -> Future[STATE_DICT_TYPE]:\n        staging_executor = ThreadPoolExecutor(max_workers=1)\n        if isinstance(storage_writer, AsyncStager) and not use_default_staging:",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2159408147",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156207,
        "pr_file": "torch/distributed/checkpoint/state_dict_saver.py",
        "discussion_id": "2159408147",
        "commented_code": "@@ -249,49 +305,70 @@ def async_save(\n             \"A CPU backend must be enabled for async save; try initializing process group with 'cpu:gloo,cuda:nccl'\"\n         )\n \n+    use_default_staging = False\n+    if storage_writer is None:\n+        use_default_staging = True\n+\n     storage_writer = cast(\n         StorageWriter, _storage_setup(storage_writer, checkpoint_id, reader=False)\n     )\n \n     state_dict = _stateful_to_state_dict(state_dict)\n \n     @_dcp_method_logger(log_exceptions=True)\n-    def stage_state_dict():\n-        if isinstance(storage_writer, AsyncStager):\n-            staged_state_dict = storage_writer.stage(state_dict)\n-        else:  # provides bwc for storage_writers not implementing AsyncStager\n-            staged_state_dict = _create_cpu_state_dict(state_dict)\n-            _copy_state_dict(state_dict, staged_state_dict, type_check=False)\n-\n-        return staged_state_dict\n-\n-    staged_state_dict = stage_state_dict()\n-\n-    executor: _AsyncCheckpointExecutor = (\n+    def stage_state_dict() -> Future[STATE_DICT_TYPE]:\n+        staging_executor = ThreadPoolExecutor(max_workers=1)\n+        if isinstance(storage_writer, AsyncStager) and not use_default_staging:",
        "comment_created_at": "2025-06-20T17:16:56+00:00",
        "comment_author": "teja-rao",
        "comment_body": "```suggestion\r\n        if storage_writer is not None and  isinstance(storage_writer, AsyncStager):\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
