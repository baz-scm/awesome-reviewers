---
title: Document all parameters
description: Always provide complete and accurate documentation for all function parameters,
  especially when adding new ones. Each parameter should have a clear description
  that explains its purpose, expected values, and behavior.
repository: apache/mxnet
label: Documentation
language: Other
comments_count: 5
repository_stars: 20801
---

Always provide complete and accurate documentation for all function parameters, especially when adding new ones. Each parameter should have a clear description that explains its purpose, expected values, and behavior.

When adding a new parameter to an existing function:
1. Add documentation that clearly states what the parameter does
2. Explain any default behavior or special conditions
3. Use consistent formatting across similar functions

For example, when adding a parameter like `failsafe`:

```cpp
/**
 * \brief Allocation.
 * \param handle Handle struct.
 * \param failsafe Return a handle with a null dptr if out of memory, rather than exit.
 */
virtual void Alloc(Storage::Handle* handle, bool failsafe = false);
```

This helps other developers understand how to use the function correctly and makes the codebase more maintainable. Incomplete parameter documentation can lead to misuse of functions and introduces bugs that are difficult to diagnose.


[
  {
    "discussion_id": "845789888",
    "pr_number": 20983,
    "pr_file": "include/mxnet/c_api.h",
    "created_at": "2022-04-08T06:52:59+00:00",
    "commented_code": "* \\return 0 when success, -1 when failure happens\n */\nMXNET_DLL int MXAutogradIsTraining(bool* curr);\n/*!\n * \\brief set whether to disable AMP\n * \\param curr returns the current status",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "845789888",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20983,
        "pr_file": "include/mxnet/c_api.h",
        "discussion_id": "845789888",
        "commented_code": "@@ -1225,6 +1225,18 @@ MXNET_DLL int MXAutogradIsRecording(bool* curr);\n  * \\return 0 when success, -1 when failure happens\n  */\n MXNET_DLL int MXAutogradIsTraining(bool* curr);\n+/*!\n+ * \\brief set whether to disable AMP\n+ * \\param curr returns the current status",
        "comment_created_at": "2022-04-08T06:52:59+00:00",
        "comment_author": "bgawrych",
        "comment_body": "```suggestion\r\n * \\param prev returns the current status\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "845790273",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20983,
        "pr_file": "include/mxnet/c_api.h",
        "discussion_id": "845789888",
        "commented_code": "@@ -1225,6 +1225,18 @@ MXNET_DLL int MXAutogradIsRecording(bool* curr);\n  * \\return 0 when success, -1 when failure happens\n  */\n MXNET_DLL int MXAutogradIsTraining(bool* curr);\n+/*!\n+ * \\brief set whether to disable AMP\n+ * \\param curr returns the current status",
        "comment_created_at": "2022-04-08T06:53:36+00:00",
        "comment_author": "bgawrych",
        "comment_body": "lack of is_amp_disabled in doc",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "744059733",
    "pr_number": 20635,
    "pr_file": "include/mxnet/storage.h",
    "created_at": "2021-11-06T02:51:51+00:00",
    "commented_code": "* \\param ctx Context information about the device and ID.\n   * \\return Handle struct.\n   */\n  Handle Alloc(size_t size, Context ctx) {\n  Handle Alloc(size_t size, Context ctx, bool failsafe = false) {",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "744059733",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20635,
        "pr_file": "include/mxnet/storage.h",
        "discussion_id": "744059733",
        "commented_code": "@@ -71,18 +71,18 @@ class Storage {\n    * \\param ctx Context information about the device and ID.\n    * \\return Handle struct.\n    */\n-  Handle Alloc(size_t size, Context ctx) {\n+  Handle Alloc(size_t size, Context ctx, bool failsafe = false) {",
        "comment_created_at": "2021-11-06T02:51:51+00:00",
        "comment_author": "DickJC123",
        "comment_body": "Where you've add the failsafe parameter (here and elsewhere), please add documentation.  I suggest:\r\n\r\n \\* \\param failsafe Return a handle with a null dptr if out of memory, rather than exit.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "744071053",
    "pr_number": 20635,
    "pr_file": "src/storage/gpu_device_storage.h",
    "created_at": "2021-11-06T03:52:45+00:00",
    "commented_code": "* \\brief Allocation.\n   * \\param handle Handle struct.\n   */\n  inline static void Alloc(Storage::Handle* handle);\n  inline static void Alloc(Storage::Handle* handle, bool failsafe = false);",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "744071053",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20635,
        "pr_file": "src/storage/gpu_device_storage.h",
        "discussion_id": "744071053",
        "commented_code": "@@ -39,21 +39,28 @@ class GPUDeviceStorage {\n    * \\brief Allocation.\n    * \\param handle Handle struct.\n    */\n-  inline static void Alloc(Storage::Handle* handle);\n+  inline static void Alloc(Storage::Handle* handle, bool failsafe = false);",
        "comment_created_at": "2021-11-06T03:52:45+00:00",
        "comment_author": "DickJC123",
        "comment_body": "Add doc of new param `failsafe` per earlier comment.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "744071104",
    "pr_number": 20635,
    "pr_file": "src/storage/pinned_memory_storage.h",
    "created_at": "2021-11-06T03:53:29+00:00",
    "commented_code": "* \\brief Allocation.\n   * \\param handle Handle struct.\n   */\n  inline static void Alloc(Storage::Handle* handle);\n  inline static void Alloc(Storage::Handle* handle, bool failsafe);",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "744071104",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20635,
        "pr_file": "src/storage/pinned_memory_storage.h",
        "discussion_id": "744071104",
        "commented_code": "@@ -36,7 +36,7 @@ class PinnedMemoryStorage {\n    * \\brief Allocation.\n    * \\param handle Handle struct.\n    */\n-  inline static void Alloc(Storage::Handle* handle);\n+  inline static void Alloc(Storage::Handle* handle, bool failsafe);",
        "comment_created_at": "2021-11-06T03:53:29+00:00",
        "comment_author": "DickJC123",
        "comment_body": "Add doc of new param `failsafe` per earlier comment.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "744071143",
    "pr_number": 20635,
    "pr_file": "src/storage/storage_manager.h",
    "created_at": "2021-11-06T03:54:29+00:00",
    "commented_code": "* \\brief Allocation.\n   * \\param handle Handle struct.\n   */\n  virtual void Alloc(Storage::Handle* handle) = 0;\n  virtual void Alloc(Storage::Handle* handle, bool failsafe = false) = 0;",
    "repo_full_name": "apache/mxnet",
    "discussion_comments": [
      {
        "comment_id": "744071143",
        "repo_full_name": "apache/mxnet",
        "pr_number": 20635,
        "pr_file": "src/storage/storage_manager.h",
        "discussion_id": "744071143",
        "commented_code": "@@ -40,7 +40,7 @@ class StorageManager {\n    * \\brief Allocation.\n    * \\param handle Handle struct.\n    */\n-  virtual void Alloc(Storage::Handle* handle) = 0;\n+  virtual void Alloc(Storage::Handle* handle, bool failsafe = false) = 0;",
        "comment_created_at": "2021-11-06T03:54:29+00:00",
        "comment_author": "DickJC123",
        "comment_body": "Add doc of new param `failsafe` per earlier comment.",
        "pr_file_module": null
      }
    ]
  }
]
