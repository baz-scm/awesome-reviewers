---
title: Keep APIs user-centric simple
description: Design APIs with a focus on simplicity and user experience, especially
  for first-time users. Complex functionality should be encapsulated in well-structured
  protocols or classes rather than exposed through numerous optional parameters.
repository: pytorch/pytorch
label: API
language: Python
comments_count: 4
repository_stars: 91169
---

Design APIs with a focus on simplicity and user experience, especially for first-time users. Complex functionality should be encapsulated in well-structured protocols or classes rather than exposed through numerous optional parameters.

Key principles:
1. Avoid loose, contextless function calls (e.g. global `close()`)
2. Encapsulate related parameters in protocol/class properties
3. Keep basic usage simple while allowing advanced configurations
4. Place complex functionality behind clear abstractions

Example - Instead of:
```python
def async_save(
    state_dict,
    storage_writer,
    async_stager=None,
    block_on_staging=True,
    process_group=None,
    async_checkpointer_type=AsyncCheckpointerType.THREAD,
):
    # Complex implementation
```

Better approach:
```python
class AsyncStager:
    def __init__(self, config: AsyncStagerConfig):
        self.block_on_staging = config.block_on_staging
        self.checkpointer_type = config.checkpointer_type
        
    def async_save(self, state_dict, storage_writer):
        # Implementation with config properties
```

This makes the basic API simple while allowing advanced users to configure behavior through well-defined configuration objects.


[
  {
    "discussion_id": "2153268320",
    "pr_number": 156207,
    "pr_file": "torch/distributed/checkpoint/state_dict_saver.py",
    "created_at": "2025-06-17T22:23:21+00:00",
    "commented_code": "planner=planner,\n        )\n\ndef default_stage(state_dict: STATE_DICT_TYPE, cpu_state_dict: STATE_DICT_TYPE) -> STATE_DICT_TYPE:\n    \"\"\"Default stage function. This function will stage the state_dict on to the\n    staging storage (defaults to CPU memory).\n\n    Args:\n        state_dict STATE_DICT_TYPE: The state_dict to stage.\n\n    Returns:\n       STATE_DICT_TYPE: staged state_dict\n    \"\"\"\n    staging_stream = torch.cuda.Stream()\n    with staging_stream:\n        staged_state_dict = _copy_state_dict(state_dict, cpu_state_dict, True, type_check=False)\n    staging_stream.synchronize()\n    return staged_state_dict\n\n@dataclass\nclass AsyncSaveResponse:\n    \"\"\"This class contains futures for staging and upload completion\"\"\"\n    staging_completion: Future[None]\n    upload_completion: Future[None]\n\ndef close(): \n    \"\"\"\n        MUST CALL THIS FUNCTION AFTER TRAINING IS COMPLETE IF USING ASYNC_SAVE\n    \"\"\"",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2153268320",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156207,
        "pr_file": "torch/distributed/checkpoint/state_dict_saver.py",
        "discussion_id": "2153268320",
        "commented_code": "@@ -181,6 +189,36 @@ def save(\n             planner=planner,\n         )\n \n+def default_stage(state_dict: STATE_DICT_TYPE, cpu_state_dict: STATE_DICT_TYPE) -> STATE_DICT_TYPE:\n+    \"\"\"Default stage function. This function will stage the state_dict on to the\n+    staging storage (defaults to CPU memory).\n+\n+    Args:\n+        state_dict STATE_DICT_TYPE: The state_dict to stage.\n+\n+    Returns:\n+       STATE_DICT_TYPE: staged state_dict\n+    \"\"\"\n+    staging_stream = torch.cuda.Stream()\n+    with staging_stream:\n+        staged_state_dict = _copy_state_dict(state_dict, cpu_state_dict, True, type_check=False)\n+    staging_stream.synchronize()\n+    return staged_state_dict\n+\n+@dataclass\n+class AsyncSaveResponse:\n+    \"\"\"This class contains futures for staging and upload completion\"\"\"\n+    staging_completion: Future[None]\n+    upload_completion: Future[None]\n+\n+def close(): \n+    \"\"\"\n+        MUST CALL THIS FUNCTION AFTER TRAINING IS COMPLETE IF USING ASYNC_SAVE\n+    \"\"\"",
        "comment_created_at": "2025-06-17T22:23:21+00:00",
        "comment_author": "fegin",
        "comment_body": "Probably not a good idea to ask users to selectively call `close()`. I would suggest that users should always call `close()`. Also if this is a public API, the docstring should follow the template. You can check other docstring.",
        "pr_file_module": null
      },
      {
        "comment_id": "2153271922",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156207,
        "pr_file": "torch/distributed/checkpoint/state_dict_saver.py",
        "discussion_id": "2153268320",
        "commented_code": "@@ -181,6 +189,36 @@ def save(\n             planner=planner,\n         )\n \n+def default_stage(state_dict: STATE_DICT_TYPE, cpu_state_dict: STATE_DICT_TYPE) -> STATE_DICT_TYPE:\n+    \"\"\"Default stage function. This function will stage the state_dict on to the\n+    staging storage (defaults to CPU memory).\n+\n+    Args:\n+        state_dict STATE_DICT_TYPE: The state_dict to stage.\n+\n+    Returns:\n+       STATE_DICT_TYPE: staged state_dict\n+    \"\"\"\n+    staging_stream = torch.cuda.Stream()\n+    with staging_stream:\n+        staged_state_dict = _copy_state_dict(state_dict, cpu_state_dict, True, type_check=False)\n+    staging_stream.synchronize()\n+    return staged_state_dict\n+\n+@dataclass\n+class AsyncSaveResponse:\n+    \"\"\"This class contains futures for staging and upload completion\"\"\"\n+    staging_completion: Future[None]\n+    upload_completion: Future[None]\n+\n+def close(): \n+    \"\"\"\n+        MUST CALL THIS FUNCTION AFTER TRAINING IS COMPLETE IF USING ASYNC_SAVE\n+    \"\"\"",
        "comment_created_at": "2025-06-17T22:27:10+00:00",
        "comment_author": "fegin",
        "comment_body": "Should we also wait for the last `async_save` inside this API as well?",
        "pr_file_module": null
      },
      {
        "comment_id": "2153341662",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156207,
        "pr_file": "torch/distributed/checkpoint/state_dict_saver.py",
        "discussion_id": "2153268320",
        "commented_code": "@@ -181,6 +189,36 @@ def save(\n             planner=planner,\n         )\n \n+def default_stage(state_dict: STATE_DICT_TYPE, cpu_state_dict: STATE_DICT_TYPE) -> STATE_DICT_TYPE:\n+    \"\"\"Default stage function. This function will stage the state_dict on to the\n+    staging storage (defaults to CPU memory).\n+\n+    Args:\n+        state_dict STATE_DICT_TYPE: The state_dict to stage.\n+\n+    Returns:\n+       STATE_DICT_TYPE: staged state_dict\n+    \"\"\"\n+    staging_stream = torch.cuda.Stream()\n+    with staging_stream:\n+        staged_state_dict = _copy_state_dict(state_dict, cpu_state_dict, True, type_check=False)\n+    staging_stream.synchronize()\n+    return staged_state_dict\n+\n+@dataclass\n+class AsyncSaveResponse:\n+    \"\"\"This class contains futures for staging and upload completion\"\"\"\n+    staging_completion: Future[None]\n+    upload_completion: Future[None]\n+\n+def close(): \n+    \"\"\"\n+        MUST CALL THIS FUNCTION AFTER TRAINING IS COMPLETE IF USING ASYNC_SAVE\n+    \"\"\"",
        "comment_created_at": "2025-06-17T23:44:42+00:00",
        "comment_author": "Saiteja64",
        "comment_body": "I think we should just leave that to the users. In general, I want to limit global training state within DCP as much as possible. ",
        "pr_file_module": null
      },
      {
        "comment_id": "2159417737",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156207,
        "pr_file": "torch/distributed/checkpoint/state_dict_saver.py",
        "discussion_id": "2153268320",
        "commented_code": "@@ -181,6 +189,36 @@ def save(\n             planner=planner,\n         )\n \n+def default_stage(state_dict: STATE_DICT_TYPE, cpu_state_dict: STATE_DICT_TYPE) -> STATE_DICT_TYPE:\n+    \"\"\"Default stage function. This function will stage the state_dict on to the\n+    staging storage (defaults to CPU memory).\n+\n+    Args:\n+        state_dict STATE_DICT_TYPE: The state_dict to stage.\n+\n+    Returns:\n+       STATE_DICT_TYPE: staged state_dict\n+    \"\"\"\n+    staging_stream = torch.cuda.Stream()\n+    with staging_stream:\n+        staged_state_dict = _copy_state_dict(state_dict, cpu_state_dict, True, type_check=False)\n+    staging_stream.synchronize()\n+    return staged_state_dict\n+\n+@dataclass\n+class AsyncSaveResponse:\n+    \"\"\"This class contains futures for staging and upload completion\"\"\"\n+    staging_completion: Future[None]\n+    upload_completion: Future[None]\n+\n+def close(): \n+    \"\"\"\n+        MUST CALL THIS FUNCTION AFTER TRAINING IS COMPLETE IF USING ASYNC_SAVE\n+    \"\"\"",
        "comment_created_at": "2025-06-20T17:24:22+00:00",
        "comment_author": "teja-rao",
        "comment_body": "Can we cache the state in AsyncStager and let user manage the lifetime of async stager? this will allow user to init async stager and destroy as needed. this can be done on every checkpoint or at the end of the job as the user sees fit.\r\n\r\nNow, close() method is out of context. It is not on any resource/obj. It is hard for users to understand what close means and why they have to call it. \r\n\r\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2159421534",
    "pr_number": 156207,
    "pr_file": "torch/distributed/checkpoint/state_dict_saver.py",
    "created_at": "2025-06-20T17:27:28+00:00",
    "commented_code": "\"A CPU backend must be enabled for async save; try initializing process group with 'cpu:gloo,cuda:nccl'\"\n        )\n\n    use_default_staging = False\n    if storage_writer is None:\n        use_default_staging = True\n\n    storage_writer = cast(\n        StorageWriter, _storage_setup(storage_writer, checkpoint_id, reader=False)\n    )\n\n    state_dict = _stateful_to_state_dict(state_dict)\n\n    @_dcp_method_logger(log_exceptions=True)\n    def stage_state_dict():\n        if isinstance(storage_writer, AsyncStager):\n            staged_state_dict = storage_writer.stage(state_dict)\n        else:  # provides bwc for storage_writers not implementing AsyncStager\n            staged_state_dict = _create_cpu_state_dict(state_dict)\n            _copy_state_dict(state_dict, staged_state_dict, type_check=False)\n\n        return staged_state_dict\n\n    staged_state_dict = stage_state_dict()\n\n    executor: _AsyncCheckpointExecutor = (\n    def stage_state_dict() -> Future[STATE_DICT_TYPE]:\n        staging_executor = ThreadPoolExecutor(max_workers=1)\n        if isinstance(storage_writer, AsyncStager) and not use_default_staging:\n            staging_future = staging_executor.submit(storage_writer.stage, state_dict)\n        else:\n            # provides bwc for storage_writers not implementing AsyncStager",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2159421534",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156207,
        "pr_file": "torch/distributed/checkpoint/state_dict_saver.py",
        "discussion_id": "2159421534",
        "commented_code": "@@ -249,49 +305,70 @@ def async_save(\n             \"A CPU backend must be enabled for async save; try initializing process group with 'cpu:gloo,cuda:nccl'\"\n         )\n \n+    use_default_staging = False\n+    if storage_writer is None:\n+        use_default_staging = True\n+\n     storage_writer = cast(\n         StorageWriter, _storage_setup(storage_writer, checkpoint_id, reader=False)\n     )\n \n     state_dict = _stateful_to_state_dict(state_dict)\n \n     @_dcp_method_logger(log_exceptions=True)\n-    def stage_state_dict():\n-        if isinstance(storage_writer, AsyncStager):\n-            staged_state_dict = storage_writer.stage(state_dict)\n-        else:  # provides bwc for storage_writers not implementing AsyncStager\n-            staged_state_dict = _create_cpu_state_dict(state_dict)\n-            _copy_state_dict(state_dict, staged_state_dict, type_check=False)\n-\n-        return staged_state_dict\n-\n-    staged_state_dict = stage_state_dict()\n-\n-    executor: _AsyncCheckpointExecutor = (\n+    def stage_state_dict() -> Future[STATE_DICT_TYPE]:\n+        staging_executor = ThreadPoolExecutor(max_workers=1)\n+        if isinstance(storage_writer, AsyncStager) and not use_default_staging:\n+            staging_future = staging_executor.submit(storage_writer.stage, state_dict)\n+        else:\n+            # provides bwc for storage_writers not implementing AsyncStager",
        "comment_created_at": "2025-06-20T17:27:28+00:00",
        "comment_author": "teja-rao",
        "comment_body": "do we need to handle this case? can we ask user to implement async stager if they need to use zero-copy? I think it is simpler to support and cleaner from API point of view. ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2167615520",
    "pr_number": 156207,
    "pr_file": "torch/distributed/checkpoint/state_dict_saver.py",
    "created_at": "2025-06-25T20:54:34+00:00",
    "commented_code": "planner: Optional[SavePlanner] = None,\n    process_group: Optional[dist.ProcessGroup] = None,\n    async_checkpointer_type: AsyncCheckpointerType = AsyncCheckpointerType.THREAD,\n) -> Future:\n    async_stager: Optional[AsyncStager] = None,\n    block_on_staging: bool = True,",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2167615520",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156207,
        "pr_file": "torch/distributed/checkpoint/state_dict_saver.py",
        "discussion_id": "2167615520",
        "commented_code": "@@ -191,12 +210,15 @@ def async_save(\n     planner: Optional[SavePlanner] = None,\n     process_group: Optional[dist.ProcessGroup] = None,\n     async_checkpointer_type: AsyncCheckpointerType = AsyncCheckpointerType.THREAD,\n-) -> Future:\n+    async_stager: Optional[AsyncStager] = None,\n+    block_on_staging: bool = True,",
        "comment_created_at": "2025-06-25T20:54:34+00:00",
        "comment_author": "meetv18",
        "comment_body": "One suggestion: \r\n\r\nCan we have these as a property in AsyncStager protocol, instead of directly bloating the API. These are mainly for power users, a simple/first time user will probably be perplexed by additional params that aren't self explanatory. ",
        "pr_file_module": null
      },
      {
        "comment_id": "2167979087",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156207,
        "pr_file": "torch/distributed/checkpoint/state_dict_saver.py",
        "discussion_id": "2167615520",
        "commented_code": "@@ -191,12 +210,15 @@ def async_save(\n     planner: Optional[SavePlanner] = None,\n     process_group: Optional[dist.ProcessGroup] = None,\n     async_checkpointer_type: AsyncCheckpointerType = AsyncCheckpointerType.THREAD,\n-) -> Future:\n+    async_stager: Optional[AsyncStager] = None,\n+    block_on_staging: bool = True,",
        "comment_created_at": "2025-06-26T02:34:55+00:00",
        "comment_author": "Saiteja64",
        "comment_body": "For async_stager argument, this is a directional change. We are separating out the stager from storage_writer. Conceptually, you should be able to use a stager with any storage_writer. Combining the two just forces us and users to change StorageWriter every time we want to make a change to stager (new properties, etc)\r\n\r\nblock_on_staging: Think we can remove this one. Works for all cases and simplifies API:\r\n1. If user configures AsyncStager to return a future instead of a state_dict, driver code can just return that future. \r\n2. If AsyncStager returns state_dict we can just keep existing logic of checking synchronize_after_execute and call synchronize_staging if needed",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1939922583",
    "pr_number": 145000,
    "pr_file": "torch/__init__.py",
    "created_at": "2025-02-03T19:34:21+00:00",
    "commented_code": "matrix_rank,\n    solve,\n)\nfrom torch.utils.dlpack import from_dlpack, to_dlpack\nfrom torch.utils.dlpack import from_dlpack, to_dlpack, to_dlpack_unversioned",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "1939922583",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 145000,
        "pr_file": "torch/__init__.py",
        "discussion_id": "1939922583",
        "commented_code": "@@ -2270,7 +2270,7 @@ def compiled_with_cxx11_abi() -> builtins.bool:\n     matrix_rank,\n     solve,\n )\n-from torch.utils.dlpack import from_dlpack, to_dlpack\n+from torch.utils.dlpack import from_dlpack, to_dlpack, to_dlpack_unversioned",
        "comment_created_at": "2025-02-03T19:34:21+00:00",
        "comment_author": "albanD",
        "comment_body": "While I understand this matches current code, I don't think we want to have this as a new top level API? Being part of torch.utils.dlpack is enough?",
        "pr_file_module": null
      },
      {
        "comment_id": "1941436061",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 145000,
        "pr_file": "torch/__init__.py",
        "discussion_id": "1939922583",
        "commented_code": "@@ -2270,7 +2270,7 @@ def compiled_with_cxx11_abi() -> builtins.bool:\n     matrix_rank,\n     solve,\n )\n-from torch.utils.dlpack import from_dlpack, to_dlpack\n+from torch.utils.dlpack import from_dlpack, to_dlpack, to_dlpack_unversioned",
        "comment_created_at": "2025-02-04T15:50:51+00:00",
        "comment_author": "rgommers",
        "comment_body": "That comment sounds right - I don't think it should be needed. For the introduction strategy to a versioned protocol, see the explanation and prototype code (`if max_version is None: ....`) at https://data-apis.org/array-api/latest/API_specification/generated/array_api.array.__dlpack__.html",
        "pr_file_module": null
      },
      {
        "comment_id": "1941444094",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 145000,
        "pr_file": "torch/__init__.py",
        "discussion_id": "1939922583",
        "commented_code": "@@ -2270,7 +2270,7 @@ def compiled_with_cxx11_abi() -> builtins.bool:\n     matrix_rank,\n     solve,\n )\n-from torch.utils.dlpack import from_dlpack, to_dlpack\n+from torch.utils.dlpack import from_dlpack, to_dlpack, to_dlpack_unversioned",
        "comment_created_at": "2025-02-04T15:55:19+00:00",
        "comment_author": "rgommers",
        "comment_body": "If it's useful/needed to have a Python function to use here so that can be called from within `Tensor.__dlpack__`, then making it a private function by prepending an underscore should be fine I think.",
        "pr_file_module": null
      }
    ]
  }
]
