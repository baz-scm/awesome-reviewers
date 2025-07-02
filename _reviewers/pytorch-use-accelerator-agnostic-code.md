---
title: Use accelerator-agnostic code
description: Write code that works across different hardware accelerators by using
  PyTorch's accelerator abstraction API rather than hardcoding device-specific logic.
  This prevents failures when code runs on different hardware platforms like CPU,
  CUDA, ROCm, or other accelerators.
repository: pytorch/pytorch
label: Pytorch
language: Python
comments_count: 12
repository_stars: 91169
---

Write code that works across different hardware accelerators by using PyTorch's accelerator abstraction API rather than hardcoding device-specific logic. This prevents failures when code runs on different hardware platforms like CPU, CUDA, ROCm, or other accelerators.

Instead of checking for specific device types or hardcoding device names:

```python
# Problematic: Device-specific code
if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"
tensor = torch.randn(3, 3).cuda()  # Fails on non-CUDA systems
```

Use the accelerator API for device detection and management:

```python
# Better: Accelerator-agnostic code
device = (torch.accelerator.current_accelerator().type 
          if torch.accelerator.is_available() 
          else "cpu")
tensor = torch.randn(3, 3).to(device)  # Works on any system
```

When writing tests, avoid assuming specific devices:

```python
# Instead of:
@requires_cuda
def test_feature():
    x = torch.randn(3, 3).cuda()
    # test code

# Do this:
@requires_accelerator
def test_feature():
    device = torch.accelerator.current_accelerator().type
    x = torch.randn(3, 3).to(device)
    # test code
```

By writing accelerator-agnostic code, you ensure your PyTorch code works consistently across different hardware platforms without modification.


[
  {
    "discussion_id": "2177758844",
    "pr_number": 156287,
    "pr_file": "torch/_functorch/partitioners.py",
    "created_at": "2025-07-01T14:28:29+00:00",
    "commented_code": "):\n        with no_dispatch(), unset_fake_temporarily():\n            objects = [[x.name for x in saved_values]]\n            # TODO: maybe use a different process group for this\n            torch.distributed.broadcast_object_list(objects, src=0)\n            saved_values_names = objects[0]\n            saved_ops_names_all_ranks: list[list[str]] = [\n                [] for _ in range(torch.distributed.get_world_size())\n            ]\n\n            torch.distributed.all_gather_object(saved_ops_names_all_ranks, objects[0])\n            name_to_node = get_name_to_node(joint_graph)\n            saved_values = [name_to_node[n] for n in saved_values_names]\n            saved_sizes: list[int] = []\n            for saved_ops_names in saved_ops_names_all_ranks:\n                saved_nodes = [name_to_node[op_name] for op_name in saved_ops_names]\n                saved_size = 0\n                for node in saved_nodes:\n                    saved_size += _size_of(node)\n                saved_sizes.append(saved_size)\n\n            saved_sizes_tensor = torch.tensor(\n                saved_sizes, device=torch.cuda.current_device()",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2177758844",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156287,
        "pr_file": "torch/_functorch/partitioners.py",
        "discussion_id": "2177758844",
        "commented_code": "@@ -2515,11 +2515,38 @@ def has_same_nodes(joint_graph):\n     ):\n         with no_dispatch(), unset_fake_temporarily():\n             objects = [[x.name for x in saved_values]]\n-            # TODO: maybe use a different process group for this\n-            torch.distributed.broadcast_object_list(objects, src=0)\n-            saved_values_names = objects[0]\n+            saved_ops_names_all_ranks: list[list[str]] = [\n+                [] for _ in range(torch.distributed.get_world_size())\n+            ]\n+\n+            torch.distributed.all_gather_object(saved_ops_names_all_ranks, objects[0])\n             name_to_node = get_name_to_node(joint_graph)\n-            saved_values = [name_to_node[n] for n in saved_values_names]\n+            saved_sizes: list[int] = []\n+            for saved_ops_names in saved_ops_names_all_ranks:\n+                saved_nodes = [name_to_node[op_name] for op_name in saved_ops_names]\n+                saved_size = 0\n+                for node in saved_nodes:\n+                    saved_size += _size_of(node)\n+                saved_sizes.append(saved_size)\n+\n+            saved_sizes_tensor = torch.tensor(\n+                saved_sizes, device=torch.cuda.current_device()",
        "comment_created_at": "2025-07-01T14:28:29+00:00",
        "comment_author": "bdhirsh",
        "comment_body": "Instead of hardcoding the cuda device here, can we try to use the same device that our collectives are going to use?\r\n\r\nMaybe @wconstab knows of a cleaner way, but it looks like `all_gather_object` figures out what device to use with [this](https://github.com/pytorch/pytorch/blob/main/torch/distributed/distributed_c10d.py#L3153C5-L3153C52)\r\n```\r\ncurrent_device = _get_object_coll_device(_group_or_default_group())\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2179128797",
    "pr_number": 155108,
    "pr_file": "test/distributed/pipelining/test_backward.py",
    "created_at": "2025-07-02T05:14:19+00:00",
    "commented_code": "stage_backward_input,\n    stage_backward_weight,\n)\nfrom torch.testing._internal.common_device_type import instantiate_device_type_tests\nfrom torch.testing._internal.common_utils import run_tests, TestCase\n\n\nd_hid = 512\nbatch_size = 256\n\ndevice = torch.accelerator.current_accelerator().type",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2179128797",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 155108,
        "pr_file": "test/distributed/pipelining/test_backward.py",
        "discussion_id": "2179128797",
        "commented_code": "@@ -10,16 +10,17 @@\n     stage_backward_input,\n     stage_backward_weight,\n )\n-from torch.testing._internal.common_device_type import instantiate_device_type_tests\n from torch.testing._internal.common_utils import run_tests, TestCase\n \n \n d_hid = 512\n batch_size = 256\n \n+device = torch.accelerator.current_accelerator().type",
        "comment_created_at": "2025-07-02T05:14:19+00:00",
        "comment_author": "guangyey",
        "comment_body": "This will fail on the CPU-only machine.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2179130007",
    "pr_number": 155108,
    "pr_file": "test/distributed/pipelining/test_backward.py",
    "created_at": "2025-07-02T05:15:18+00:00",
    "commented_code": "stage_backward_input,\n    stage_backward_weight,\n)\nfrom torch.testing._internal.common_device_type import instantiate_device_type_tests\nfrom torch.testing._internal.common_utils import run_tests, TestCase\n\n\nd_hid = 512\nbatch_size = 256\n\ndevice = torch.accelerator.current_accelerator().type",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2179130007",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 155108,
        "pr_file": "test/distributed/pipelining/test_backward.py",
        "discussion_id": "2179130007",
        "commented_code": "@@ -10,16 +10,17 @@\n     stage_backward_input,\n     stage_backward_weight,\n )\n-from torch.testing._internal.common_device_type import instantiate_device_type_tests\n from torch.testing._internal.common_utils import run_tests, TestCase\n \n \n d_hid = 512\n batch_size = 256\n \n+device = torch.accelerator.current_accelerator().type",
        "comment_created_at": "2025-07-02T05:15:18+00:00",
        "comment_author": "guangyey",
        "comment_body": "```suggestion\r\ndevice = acc.type if (acc := torch.accelerator.current_accelerator()) else \"cpu\"\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2179135225",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 155108,
        "pr_file": "test/distributed/pipelining/test_backward.py",
        "discussion_id": "2179130007",
        "commented_code": "@@ -10,16 +10,17 @@\n     stage_backward_input,\n     stage_backward_weight,\n )\n-from torch.testing._internal.common_device_type import instantiate_device_type_tests\n from torch.testing._internal.common_utils import run_tests, TestCase\n \n \n d_hid = 512\n batch_size = 256\n \n+device = torch.accelerator.current_accelerator().type",
        "comment_created_at": "2025-07-02T05:19:14+00:00",
        "comment_author": "AnantGulati",
        "comment_body": "As per my understanding, since pipeline parallelism is dependent on communication collectives supported only for accelerator backends, not by GLOO hence we would not want to test on CPU\r\n\r\n@H-Huang Could you please confirm\r\n\r\nThanks ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2176247028",
    "pr_number": 157317,
    "pr_file": "torch/distributed/tensor/examples/visualize_sharding_example.py",
    "created_at": "2025-07-01T01:56:31+00:00",
    "commented_code": "assert int(os.getenv(\"WORLD_SIZE\", \"1\")) >= 4, \"We need at least 4 devices\"\nrank = int(os.environ[\"RANK\"])\n\ndef get_device_type() -> str:\n    return (\n        torch.accelerator.current_accelerator().type\n        if  torch.accelerator.current_accelerator() and torch.accelerator.device_count()\n        else \"cpu\"\n    )",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2176247028",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 157317,
        "pr_file": "torch/distributed/tensor/examples/visualize_sharding_example.py",
        "discussion_id": "2176247028",
        "commented_code": "@@ -17,6 +17,15 @@\n assert int(os.getenv(\"WORLD_SIZE\", \"1\")) >= 4, \"We need at least 4 devices\"\n rank = int(os.environ[\"RANK\"])\n \n+def get_device_type() -> str:\n+    return (\n+        torch.accelerator.current_accelerator().type\n+        if  torch.accelerator.current_accelerator() and torch.accelerator.device_count()\n+        else \"cpu\"\n+    )",
        "comment_created_at": "2025-07-01T01:56:31+00:00",
        "comment_author": "guangyey",
        "comment_body": "```suggestion\r\n    return acc.type if (acc := torch.accelerator.current_accelerator(True)) else \"cpu\"\r\n\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2176248163",
    "pr_number": 157317,
    "pr_file": "torch/distributed/tensor/examples/comm_mode_features_example.py",
    "created_at": "2025-07-01T01:58:07+00:00",
    "commented_code": "def get_device_type() -> str:\n    return (\n        \"cuda\"\n        if torch.cuda.is_available() and torch.cuda.device_count() >= 4\n        torch.accelerator.current_accelerator().type\n        if  torch.accelerator.current_accelerator() and torch.accelerator.device_count() >= 4",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2176248163",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 157317,
        "pr_file": "torch/distributed/tensor/examples/comm_mode_features_example.py",
        "discussion_id": "2176248163",
        "commented_code": "@@ -28,12 +28,13 @@\n \n def get_device_type() -> str:\n     return (\n-        \"cuda\"\n-        if torch.cuda.is_available() and torch.cuda.device_count() >= 4\n+        torch.accelerator.current_accelerator().type\n+        if  torch.accelerator.current_accelerator() and torch.accelerator.device_count() >= 4",
        "comment_created_at": "2025-07-01T01:58:07+00:00",
        "comment_author": "guangyey",
        "comment_body": "```suggestion\r\n        if torch.accelerator.device_count() >= 4\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2019529880",
    "pr_number": 149697,
    "pr_file": "torch/_inductor/scheduler.py",
    "created_at": "2025-03-28T22:54:56+00:00",
    "commented_code": "return buf_byte_accesses\n\n    @cache_on_self\n    def estimate_flops(self) -> int | None:\n        from torch._subclasses.fake_tensor import FakeTensorMode\n        from torch.utils.flop_counter import FlopCounterMode\n\n        op = kernel_name_to_op.get(getattr(self.node, \"python_kernel_name\", \"\"), None)",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2019529880",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 149697,
        "pr_file": "torch/_inductor/scheduler.py",
        "discussion_id": "2019529880",
        "commented_code": "@@ -736,6 +737,48 @@ def get_buf_bytes(\n \n         return buf_byte_accesses\n \n+    @cache_on_self\n+    def estimate_flops(self) -> int | None:\n+        from torch._subclasses.fake_tensor import FakeTensorMode\n+        from torch.utils.flop_counter import FlopCounterMode\n+\n+        op = kernel_name_to_op.get(getattr(self.node, \"python_kernel_name\", \"\"), None)",
        "comment_created_at": "2025-03-28T22:54:56+00:00",
        "comment_author": "eellison",
        "comment_body": "this should handle triton templates as well.",
        "pr_file_module": null
      },
      {
        "comment_id": "2019538427",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 149697,
        "pr_file": "torch/_inductor/scheduler.py",
        "discussion_id": "2019529880",
        "commented_code": "@@ -736,6 +737,48 @@ def get_buf_bytes(\n \n         return buf_byte_accesses\n \n+    @cache_on_self\n+    def estimate_flops(self) -> int | None:\n+        from torch._subclasses.fake_tensor import FakeTensorMode\n+        from torch.utils.flop_counter import FlopCounterMode\n+\n+        op = kernel_name_to_op.get(getattr(self.node, \"python_kernel_name\", \"\"), None)",
        "comment_created_at": "2025-03-28T23:05:13+00:00",
        "comment_author": "eellison",
        "comment_body": "can you check that we preserve flops with fusion, say mm + relu?",
        "pr_file_module": null
      },
      {
        "comment_id": "2025682278",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 149697,
        "pr_file": "torch/_inductor/scheduler.py",
        "discussion_id": "2019529880",
        "commented_code": "@@ -736,6 +737,48 @@ def get_buf_bytes(\n \n         return buf_byte_accesses\n \n+    @cache_on_self\n+    def estimate_flops(self) -> int | None:\n+        from torch._subclasses.fake_tensor import FakeTensorMode\n+        from torch.utils.flop_counter import FlopCounterMode\n+\n+        op = kernel_name_to_op.get(getattr(self.node, \"python_kernel_name\", \"\"), None)",
        "comment_created_at": "2025-04-02T22:22:55+00:00",
        "comment_author": "exclamaforte",
        "comment_body": "added",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2096875232",
    "pr_number": 153213,
    "pr_file": "torch/distributed/tensor/examples/visualize_sharding_example.py",
    "created_at": "2025-05-20T04:17:10+00:00",
    "commented_code": "assert int(os.getenv(\"WORLD_SIZE\", \"1\")) >= 4, \"We need at least 4 devices\"\nrank = int(os.environ[\"RANK\"])\n\ndevice_type = 'cpu' if not torch.accelerator.current_accelerator() else torch.accelerator.current_accelerator().type",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2096875232",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 153213,
        "pr_file": "torch/distributed/tensor/examples/visualize_sharding_example.py",
        "discussion_id": "2096875232",
        "commented_code": "@@ -17,6 +17,8 @@\n assert int(os.getenv(\"WORLD_SIZE\", \"1\")) >= 4, \"We need at least 4 devices\"\n rank = int(os.environ[\"RANK\"])\n \n+device_type = 'cpu' if not torch.accelerator.current_accelerator() else torch.accelerator.current_accelerator().type",
        "comment_created_at": "2025-05-20T04:17:10+00:00",
        "comment_author": "guangyey",
        "comment_body": "```suggestion\r\ndevice_type = 'cpu' if not torch.accelerator.is_available() else torch.accelerator.current_accelerator().type\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1836158932",
    "pr_number": 137846,
    "pr_file": "torch/utils/collect_env.py",
    "created_at": "2024-11-11T08:55:41+00:00",
    "commented_code": "debug_mode_str = str(torch.version.debug)\n        cuda_available_str = str(torch.cuda.is_available())\n        cuda_version_str = torch.version.cuda\n        xpu_available_str = str(torch.xpu.is_available())",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "1836158932",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 137846,
        "pr_file": "torch/utils/collect_env.py",
        "discussion_id": "1836158932",
        "commented_code": "@@ -458,6 +592,7 @@ def get_env_info():\n         debug_mode_str = str(torch.version.debug)\n         cuda_available_str = str(torch.cuda.is_available())\n         cuda_version_str = torch.version.cuda\n+        xpu_available_str = str(torch.xpu.is_available())",
        "comment_created_at": "2024-11-11T08:55:41+00:00",
        "comment_author": "guangyey",
        "comment_body": "Now, we can use `torch.version.xpu` here.",
        "pr_file_module": null
      },
      {
        "comment_id": "1837584799",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 137846,
        "pr_file": "torch/utils/collect_env.py",
        "discussion_id": "1836158932",
        "commented_code": "@@ -458,6 +592,7 @@ def get_env_info():\n         debug_mode_str = str(torch.version.debug)\n         cuda_available_str = str(torch.cuda.is_available())\n         cuda_version_str = torch.version.cuda\n+        xpu_available_str = str(torch.xpu.is_available())",
        "comment_created_at": "2024-11-12T07:14:02+00:00",
        "comment_author": "jingxu10",
        "comment_body": "added.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1837866602",
    "pr_number": 137846,
    "pr_file": "torch/utils/collect_env.py",
    "created_at": "2024-11-12T10:33:50+00:00",
    "commented_code": "hip_runtime_version = get_version_or_na(cfg, 'HIP Runtime')\n            miopen_runtime_version = get_version_or_na(cfg, 'MIOpen')\n            cuda_version_str = 'N/A'\n            xpu_version_str = 'N/A'\n            hip_compiled_version = torch.version.hip\n    else:\n        version_str = debug_mode_str = cuda_available_str = cuda_version_str = 'N/A'\n        version_str = debug_mode_str = cuda_available_str = cuda_version_str = xpu_available_str = xpu_version_str = 'N/A'",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "1837866602",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 137846,
        "pr_file": "torch/utils/collect_env.py",
        "discussion_id": "1837866602",
        "commented_code": "@@ -511,9 +645,10 @@ def get_version_or_na(cfg, prefix):\n             hip_runtime_version = get_version_or_na(cfg, 'HIP Runtime')\n             miopen_runtime_version = get_version_or_na(cfg, 'MIOpen')\n             cuda_version_str = 'N/A'\n+            xpu_version_str = 'N/A'\n             hip_compiled_version = torch.version.hip\n     else:\n-        version_str = debug_mode_str = cuda_available_str = cuda_version_str = 'N/A'\n+        version_str = debug_mode_str = cuda_available_str = cuda_version_str = xpu_available_str = xpu_version_str = 'N/A'",
        "comment_created_at": "2024-11-12T10:33:50+00:00",
        "comment_author": "guangyey",
        "comment_body": "```suggestion\r\n        version_str = debug_mode_str = cuda_available_str = cuda_version_str = xpu_version_str = 'N/A'\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2023970199",
    "pr_number": 137846,
    "pr_file": "torch/utils/collect_env.py",
    "created_at": "2025-04-02T02:39:13+00:00",
    "commented_code": "return smi\n\n\ndef get_intel_gpu_onboard(run_lambda):\n    lst = []\n    platform = get_platform()\n    if platform == \"linux\":\n        txt = run_and_read_all(run_lambda, \"xpu-smi discovery -j\")\n        if txt:\n            try:\n                obj = json.loads(txt)\n                if type(obj[\"device_list\"]) is list:\n                    for o in obj[\"device_list\"]:\n                        lst.append(f'* {o[\"device_name\"]}')\n                else:\n                    lst.append(\"N/A\")\n            except (ValueError, TypeError) as e:\n                lst.append(str(e))\n        else:\n            lst.append(\"N/A\")\n    if platform == \"win32\" or platform == \"cygwin\":\n        txt = run_and_read_all(\n            run_lambda,\n            'powershell.exe \"gwmi -Class Win32_PnpSignedDriver | where{$_.DeviceClass -eq \\\\\"DISPLAY\\\\\"\\\n            -and $_.Manufacturer -match \\\\\"Intel\\\\\"} | Select-Object -Property DeviceName | ConvertTo-Json\"',\n        )\n        try:\n            obj = json.loads(txt)\n            if type(obj) is list:\n                for o in obj:\n                    lst.append(f'* {o[\"DeviceName\"]}')\n            else:\n                lst.append(f'* {obj[\"DeviceName\"]}')\n        except ValueError as e:\n            lst.append(txt)\n            lst.append(str(e))\n    return \"\\n\".join(lst)\n\n\ndef get_intel_gpu_detected(run_lambda):\n    if TORCH_AVAILABLE:\n        devices = [\n            f\"* [{i}] {torch.xpu.get_device_properties(i)}\"\n            for i in range(torch.xpu.device_count())\n        ]\n        if len(devices) > 0:\n            return \"\\n\".join(devices)\n        else:\n            return \"N/A\"\n    else:\n        return \"N/A\"",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2023970199",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 137846,
        "pr_file": "torch/utils/collect_env.py",
        "discussion_id": "2023970199",
        "commented_code": "@@ -243,6 +247,56 @@ def get_nvidia_smi():\n     return smi\n \n \n+def get_intel_gpu_onboard(run_lambda):\n+    lst = []\n+    platform = get_platform()\n+    if platform == \"linux\":\n+        txt = run_and_read_all(run_lambda, \"xpu-smi discovery -j\")\n+        if txt:\n+            try:\n+                obj = json.loads(txt)\n+                if type(obj[\"device_list\"]) is list:\n+                    for o in obj[\"device_list\"]:\n+                        lst.append(f'* {o[\"device_name\"]}')\n+                else:\n+                    lst.append(\"N/A\")\n+            except (ValueError, TypeError) as e:\n+                lst.append(str(e))\n+        else:\n+            lst.append(\"N/A\")\n+    if platform == \"win32\" or platform == \"cygwin\":\n+        txt = run_and_read_all(\n+            run_lambda,\n+            'powershell.exe \"gwmi -Class Win32_PnpSignedDriver | where{$_.DeviceClass -eq \\\\\"DISPLAY\\\\\"\\\n+            -and $_.Manufacturer -match \\\\\"Intel\\\\\"} | Select-Object -Property DeviceName | ConvertTo-Json\"',\n+        )\n+        try:\n+            obj = json.loads(txt)\n+            if type(obj) is list:\n+                for o in obj:\n+                    lst.append(f'* {o[\"DeviceName\"]}')\n+            else:\n+                lst.append(f'* {obj[\"DeviceName\"]}')\n+        except ValueError as e:\n+            lst.append(txt)\n+            lst.append(str(e))\n+    return \"\\n\".join(lst)\n+\n+\n+def get_intel_gpu_detected(run_lambda):\n+    if TORCH_AVAILABLE:\n+        devices = [\n+            f\"* [{i}] {torch.xpu.get_device_properties(i)}\"\n+            for i in range(torch.xpu.device_count())\n+        ]\n+        if len(devices) > 0:\n+            return \"\\n\".join(devices)\n+        else:\n+            return \"N/A\"\n+    else:\n+        return \"N/A\"",
        "comment_created_at": "2025-04-02T02:39:13+00:00",
        "comment_author": "guangyey",
        "comment_body": "```suggestion\r\n    if not TORCH_AVAILABLE:\r\n        return \"N/A\"\r\n\r\n    device_count = torch.xpu.device_count()\r\n    if device_count == 0:\r\n        return \"N/A\"\r\n\r\n    devices = [f\"* [{i}] {torch.xpu.get_device_properties(i)}\" for i in range(device_count)]\r\n    return \"\\n\".join(devices)\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1942979749",
    "pr_number": 145136,
    "pr_file": "test/inductor/test_torchinductor.py",
    "created_at": "2025-02-05T13:49:25+00:00",
    "commented_code": "):\n                    c_op(x, kernel_size=2, stride=2)\n\n    @torch._dynamo.config.patch(recompile_limit=12)\n    def test_conv_errors_with_uint(self):\n        for dim in (1, 2, 3):\n            for dtype in (torch.uint8, torch.uint16, torch.uint32, torch.uint64):\n                input_shape = [1, 8] + [64] * dim\n                x = torch.randn(input_shape).to(dtype).cuda()\n                conv_weight = (torch.ones(8, 1, *([4] * dim)) / (4 ** dim)).cuda()",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "1942979749",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 145136,
        "pr_file": "test/inductor/test_torchinductor.py",
        "discussion_id": "1942979749",
        "commented_code": "@@ -6316,6 +6316,21 @@ def test_avg_pool_errors_with_uint(self):\n                 ):\n                     c_op(x, kernel_size=2, stride=2)\n \n+    @torch._dynamo.config.patch(recompile_limit=12)\n+    def test_conv_errors_with_uint(self):\n+        for dim in (1, 2, 3):\n+            for dtype in (torch.uint8, torch.uint16, torch.uint32, torch.uint64):\n+                input_shape = [1, 8] + [64] * dim\n+                x = torch.randn(input_shape).to(dtype).cuda()\n+                conv_weight = (torch.ones(8, 1, *([4] * dim)) / (4 ** dim)).cuda()",
        "comment_created_at": "2025-02-05T13:49:25+00:00",
        "comment_author": "etaf",
        "comment_body": "Hi, the test_torchinductor.py is shared by GPUs like `cuda`, `xpu`. But you use hard code `cuda` here so this case will failed on other GPUs. I suggest you decorate this case with `requires_cuda` or use `to(GPU_TYPE)` instead of `.cuda`.",
        "pr_file_module": null
      },
      {
        "comment_id": "1944038313",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 145136,
        "pr_file": "test/inductor/test_torchinductor.py",
        "discussion_id": "1942979749",
        "commented_code": "@@ -6316,6 +6316,21 @@ def test_avg_pool_errors_with_uint(self):\n                 ):\n                     c_op(x, kernel_size=2, stride=2)\n \n+    @torch._dynamo.config.patch(recompile_limit=12)\n+    def test_conv_errors_with_uint(self):\n+        for dim in (1, 2, 3):\n+            for dtype in (torch.uint8, torch.uint16, torch.uint32, torch.uint64):\n+                input_shape = [1, 8] + [64] * dim\n+                x = torch.randn(input_shape).to(dtype).cuda()\n+                conv_weight = (torch.ones(8, 1, *([4] * dim)) / (4 ** dim)).cuda()",
        "comment_created_at": "2025-02-06T03:21:34+00:00",
        "comment_author": "shaoyuyoung",
        "comment_body": "really thanks, I'll do this :)",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2089800822",
    "pr_number": 150218,
    "pr_file": "torch/utils/dlpack.py",
    "created_at": "2025-05-14T21:46:12+00:00",
    "commented_code": "\"\"\"\n    if hasattr(ext_tensor, '__dlpack__'):\n        kwargs: dict[str, Any] = {}\n        kwargs[\"max_version\"] = (1, 0)\n\n        device = ext_tensor.__dlpack_device__()\n        # device is either CUDA or ROCm, we need to pass the current\n        kwargs[\"max_version\"] = (1, 0)\n        kwargs[\"copy\"] = copy\n\n        # Parse the device parameter.\n        # At this moment, it can either be a torch.device or a str representing\n        # a torch.device, e.g. \"cpu\", \"cuda\", etc.\n        if device is not None:\n            if isinstance(device, str):\n                device = torch.device(device)\n            assert isinstance(device, torch.device), (\n                f\"from_dlpack: unsupported device type: {type(device)}\"\n            )\n            device = torch._C._torchDeviceToDLDevice(device)\n\n        kwargs[\"dl_device\"] = device\n\n        ext_device = ext_tensor.__dlpack_device__()\n        # ext_device is either CUDA or ROCm, we need to pass the current",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2089800822",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 150218,
        "pr_file": "torch/utils/dlpack.py",
        "discussion_id": "2089800822",
        "commented_code": "@@ -107,19 +107,34 @@ def from_dlpack(ext_tensor: Any) -> 'torch.Tensor':\n     \"\"\"\n     if hasattr(ext_tensor, '__dlpack__'):\n         kwargs: dict[str, Any] = {}\n-        kwargs[\"max_version\"] = (1, 0)\n \n-        device = ext_tensor.__dlpack_device__()\n-        # device is either CUDA or ROCm, we need to pass the current\n+        kwargs[\"max_version\"] = (1, 0)\n+        kwargs[\"copy\"] = copy\n+\n+        # Parse the device parameter.\n+        # At this moment, it can either be a torch.device or a str representing\n+        # a torch.device, e.g. \"cpu\", \"cuda\", etc.\n+        if device is not None:\n+            if isinstance(device, str):\n+                device = torch.device(device)\n+            assert isinstance(device, torch.device), (\n+                f\"from_dlpack: unsupported device type: {type(device)}\"\n+            )\n+            device = torch._C._torchDeviceToDLDevice(device)\n+\n+        kwargs[\"dl_device\"] = device\n+\n+        ext_device = ext_tensor.__dlpack_device__()\n+        # ext_device is either CUDA or ROCm, we need to pass the current",
        "comment_created_at": "2025-05-14T21:46:12+00:00",
        "comment_author": "albanD",
        "comment_body": "Note that a lot of this string handling should get generalized to any device which is an accelerator in PT.\r\nOk to do later, but as we're going to see issues with hip or xpu, we should just refactor it together",
        "pr_file_module": null
      },
      {
        "comment_id": "2105841400",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 150218,
        "pr_file": "torch/utils/dlpack.py",
        "discussion_id": "2089800822",
        "commented_code": "@@ -107,19 +107,34 @@ def from_dlpack(ext_tensor: Any) -> 'torch.Tensor':\n     \"\"\"\n     if hasattr(ext_tensor, '__dlpack__'):\n         kwargs: dict[str, Any] = {}\n-        kwargs[\"max_version\"] = (1, 0)\n \n-        device = ext_tensor.__dlpack_device__()\n-        # device is either CUDA or ROCm, we need to pass the current\n+        kwargs[\"max_version\"] = (1, 0)\n+        kwargs[\"copy\"] = copy\n+\n+        # Parse the device parameter.\n+        # At this moment, it can either be a torch.device or a str representing\n+        # a torch.device, e.g. \"cpu\", \"cuda\", etc.\n+        if device is not None:\n+            if isinstance(device, str):\n+                device = torch.device(device)\n+            assert isinstance(device, torch.device), (\n+                f\"from_dlpack: unsupported device type: {type(device)}\"\n+            )\n+            device = torch._C._torchDeviceToDLDevice(device)\n+\n+        kwargs[\"dl_device\"] = device\n+\n+        ext_device = ext_tensor.__dlpack_device__()\n+        # ext_device is either CUDA or ROCm, we need to pass the current",
        "comment_created_at": "2025-05-24T14:35:39+00:00",
        "comment_author": "ysiraichi",
        "comment_body": "Could you help me understand what string handling you are referring to? Doesn't `torch.device(device)` work with any accelerator in PT?",
        "pr_file_module": null
      },
      {
        "comment_id": "2150373765",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 150218,
        "pr_file": "torch/utils/dlpack.py",
        "discussion_id": "2089800822",
        "commented_code": "@@ -107,19 +107,34 @@ def from_dlpack(ext_tensor: Any) -> 'torch.Tensor':\n     \"\"\"\n     if hasattr(ext_tensor, '__dlpack__'):\n         kwargs: dict[str, Any] = {}\n-        kwargs[\"max_version\"] = (1, 0)\n \n-        device = ext_tensor.__dlpack_device__()\n-        # device is either CUDA or ROCm, we need to pass the current\n+        kwargs[\"max_version\"] = (1, 0)\n+        kwargs[\"copy\"] = copy\n+\n+        # Parse the device parameter.\n+        # At this moment, it can either be a torch.device or a str representing\n+        # a torch.device, e.g. \"cpu\", \"cuda\", etc.\n+        if device is not None:\n+            if isinstance(device, str):\n+                device = torch.device(device)\n+            assert isinstance(device, torch.device), (\n+                f\"from_dlpack: unsupported device type: {type(device)}\"\n+            )\n+            device = torch._C._torchDeviceToDLDevice(device)\n+\n+        kwargs[\"dl_device\"] = device\n+\n+        ext_device = ext_tensor.__dlpack_device__()\n+        # ext_device is either CUDA or ROCm, we need to pass the current",
        "comment_created_at": "2025-06-16T16:07:55+00:00",
        "comment_author": "albanD",
        "comment_body": "Only the fact that you do custom processing only for CUDA and ROCm but we have quite a few other accelerators that would require the same treatment in the future.",
        "pr_file_module": null
      },
      {
        "comment_id": "2158864989",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 150218,
        "pr_file": "torch/utils/dlpack.py",
        "discussion_id": "2089800822",
        "commented_code": "@@ -107,19 +107,34 @@ def from_dlpack(ext_tensor: Any) -> 'torch.Tensor':\n     \"\"\"\n     if hasattr(ext_tensor, '__dlpack__'):\n         kwargs: dict[str, Any] = {}\n-        kwargs[\"max_version\"] = (1, 0)\n \n-        device = ext_tensor.__dlpack_device__()\n-        # device is either CUDA or ROCm, we need to pass the current\n+        kwargs[\"max_version\"] = (1, 0)\n+        kwargs[\"copy\"] = copy\n+\n+        # Parse the device parameter.\n+        # At this moment, it can either be a torch.device or a str representing\n+        # a torch.device, e.g. \"cpu\", \"cuda\", etc.\n+        if device is not None:\n+            if isinstance(device, str):\n+                device = torch.device(device)\n+            assert isinstance(device, torch.device), (\n+                f\"from_dlpack: unsupported device type: {type(device)}\"\n+            )\n+            device = torch._C._torchDeviceToDLDevice(device)\n+\n+        kwargs[\"dl_device\"] = device\n+\n+        ext_device = ext_tensor.__dlpack_device__()\n+        # ext_device is either CUDA or ROCm, we need to pass the current",
        "comment_created_at": "2025-06-20T12:37:17+00:00",
        "comment_author": "ysiraichi",
        "comment_body": "Since I'm not familiar with these other accelerators, I think I will leave it for a future PR. In this one, I'm simply adding support for the extra keywords (in this case, passing them through to `__dlpack__()` method). What do you think?",
        "pr_file_module": null
      },
      {
        "comment_id": "2159671574",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 150218,
        "pr_file": "torch/utils/dlpack.py",
        "discussion_id": "2089800822",
        "commented_code": "@@ -107,19 +107,34 @@ def from_dlpack(ext_tensor: Any) -> 'torch.Tensor':\n     \"\"\"\n     if hasattr(ext_tensor, '__dlpack__'):\n         kwargs: dict[str, Any] = {}\n-        kwargs[\"max_version\"] = (1, 0)\n \n-        device = ext_tensor.__dlpack_device__()\n-        # device is either CUDA or ROCm, we need to pass the current\n+        kwargs[\"max_version\"] = (1, 0)\n+        kwargs[\"copy\"] = copy\n+\n+        # Parse the device parameter.\n+        # At this moment, it can either be a torch.device or a str representing\n+        # a torch.device, e.g. \"cpu\", \"cuda\", etc.\n+        if device is not None:\n+            if isinstance(device, str):\n+                device = torch.device(device)\n+            assert isinstance(device, torch.device), (\n+                f\"from_dlpack: unsupported device type: {type(device)}\"\n+            )\n+            device = torch._C._torchDeviceToDLDevice(device)\n+\n+        kwargs[\"dl_device\"] = device\n+\n+        ext_device = ext_tensor.__dlpack_device__()\n+        # ext_device is either CUDA or ROCm, we need to pass the current",
        "comment_created_at": "2025-06-20T21:13:52+00:00",
        "comment_author": "albanD",
        "comment_body": "Yes let's just open an issue for it and add the xpu and privateuse1 labels on it. ",
        "pr_file_module": null
      }
    ]
  }
]
