---
title: Descriptive meaningful names
description: Names should be clear, descriptive, and follow PyTorch's naming conventions.
  Variable names should precisely convey their purpose, avoiding ambiguity and shadowing.
  Boolean methods should use prefixes like `is_` or `has_` to indicate their nature.
repository: pytorch/pytorch
label: Naming Conventions
language: Other
comments_count: 5
repository_stars: 91169
---

Names should be clear, descriptive, and follow PyTorch's naming conventions. Variable names should precisely convey their purpose, avoiding ambiguity and shadowing. Boolean methods should use prefixes like `is_` or `has_` to indicate their nature.

Examples:
- ❌ `size_t t` → ✅ `size_t nodeIdx` or `size_t timeStep`
- ❌ `symm_mem()` → ✅ `is_symmetric()`
- ❌ `src` (shadowing) → ✅ `src_`

Always follow PyTorch's established naming conventions, avoiding camel case for variables. Properly named identifiers significantly improve code readability and maintainability, especially in open source contexts where many developers interact with the code.


[
  {
    "discussion_id": "2178202103",
    "pr_number": 157290,
    "pr_file": "torch/nativert/executor/SerialGraphExecutor.cpp",
    "created_at": "2025-07-01T17:45:50+00:00",
    "commented_code": "std::vector<c10::IValue> SerialGraphExecutor::executeWithPrefilledFrame(\n    ExecutionFrame& executionFrame) {\n  executionFrame.withMemoryPlanner([&]() {\n  executionFrame.withManagedMemory([&](const LayoutManager* m) {\n    // Execute kernels for all nodes except prim.Input and prim.Output\n    for (NodeIndex nodeIdx = 1; nodeIdx < nodeKernels_.size() - 1; ++nodeIdx) {",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2178202103",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 157290,
        "pr_file": "torch/nativert/executor/SerialGraphExecutor.cpp",
        "discussion_id": "2178202103",
        "commented_code": "@@ -14,11 +14,18 @@ std::vector<c10::IValue> SerialGraphExecutor::execute(\n \n std::vector<c10::IValue> SerialGraphExecutor::executeWithPrefilledFrame(\n     ExecutionFrame& executionFrame) {\n-  executionFrame.withMemoryPlanner([&]() {\n+  executionFrame.withManagedMemory([&](const LayoutManager* m) {\n     // Execute kernels for all nodes except prim.Input and prim.Output\n     for (NodeIndex nodeIdx = 1; nodeIdx < nodeKernels_.size() - 1; ++nodeIdx) {",
        "comment_created_at": "2025-07-01T17:45:50+00:00",
        "comment_author": "SherlockNoMad",
        "comment_body": "cc @zhxchen17 \r\n\r\nWe should follow pytorch's variable naming convention when porting code to OSS. \r\nShould do one pass for cleaning up camel case? \r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "2178737967",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 157290,
        "pr_file": "torch/nativert/executor/SerialGraphExecutor.cpp",
        "discussion_id": "2178202103",
        "commented_code": "@@ -14,11 +14,18 @@ std::vector<c10::IValue> SerialGraphExecutor::execute(\n \n std::vector<c10::IValue> SerialGraphExecutor::executeWithPrefilledFrame(\n     ExecutionFrame& executionFrame) {\n-  executionFrame.withMemoryPlanner([&]() {\n+  executionFrame.withManagedMemory([&](const LayoutManager* m) {\n     // Execute kernels for all nodes except prim.Input and prim.Output\n     for (NodeIndex nodeIdx = 1; nodeIdx < nodeKernels_.size() - 1; ++nodeIdx) {",
        "comment_created_at": "2025-07-01T23:51:25+00:00",
        "comment_author": "dolpm",
        "comment_body": "100%",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2178599052",
    "pr_number": 157290,
    "pr_file": "torch/nativert/executor/memory/LayoutManager.cpp",
    "created_at": "2025-07-01T21:50:28+00:00",
    "commented_code": "}\n}\n\n#ifndef NDEBUG\nvoid LayoutManager::assert_no_overlapping_storages(const Node& node, size_t t)",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2178599052",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 157290,
        "pr_file": "torch/nativert/executor/memory/LayoutManager.cpp",
        "discussion_id": "2178599052",
        "commented_code": "@@ -157,6 +160,121 @@ void LayoutManager::populate_tensor_values() {\n   }\n }\n \n+#ifndef NDEBUG\n+void LayoutManager::assert_no_overlapping_storages(const Node& node, size_t t)",
        "comment_created_at": "2025-07-01T21:50:28+00:00",
        "comment_author": "SherlockNoMad",
        "comment_body": "man... what's the meaning of size_t t?\r\n\r\nI have to check the call site, it says nodeIdx? \r\n\r\nPlease give meaningful names to variable. \r\n\r\nreadability really matters, especially when this code is now is OSS",
        "pr_file_module": null
      },
      {
        "comment_id": "2178747280",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 157290,
        "pr_file": "torch/nativert/executor/memory/LayoutManager.cpp",
        "discussion_id": "2178599052",
        "commented_code": "@@ -157,6 +160,121 @@ void LayoutManager::populate_tensor_values() {\n   }\n }\n \n+#ifndef NDEBUG\n+void LayoutManager::assert_no_overlapping_storages(const Node& node, size_t t)",
        "comment_created_at": "2025-07-02T00:05:19+00:00",
        "comment_author": "dolpm",
        "comment_body": "t for time. this is bad naming, i agree.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2024110858",
    "pr_number": 150506,
    "pr_file": "aten/src/ATen/native/TensorAdvancedIndexing.cpp",
    "created_at": "2025-04-02T05:48:38+00:00",
    "commented_code": "AdvancedIndex::AdvancedIndex(const Tensor& src, TensorList indices_list) {",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2024110858",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 150506,
        "pr_file": "aten/src/ATen/native/TensorAdvancedIndexing.cpp",
        "discussion_id": "2024110858",
        "commented_code": "@@ -647,14 +647,14 @@ static Tensor reshape_indexer(\n \n AdvancedIndex::AdvancedIndex(const Tensor& src, TensorList indices_list) {",
        "comment_created_at": "2025-04-02T05:48:38+00:00",
        "comment_author": "malfet",
        "comment_body": "Why not change `src` name to `src_` to avoid shadowing?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2024113352",
    "pr_number": 150506,
    "pr_file": "aten/src/ATen/native/TensorAdvancedIndexing.cpp",
    "created_at": "2025-04-02T05:51:11+00:00",
    "commented_code": "IntArrayRef a, IntArrayRef b, int64_t dim) -> bool {",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2024113352",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 150506,
        "pr_file": "aten/src/ATen/native/TensorAdvancedIndexing.cpp",
        "discussion_id": "2024113352",
        "commented_code": "@@ -1224,7 +1231,7 @@ TORCH_IMPL_FUNC(index_add_cpu_out)\n               IntArrayRef a, IntArrayRef b, int64_t dim) -> bool {",
        "comment_created_at": "2025-04-02T05:51:11+00:00",
        "comment_author": "malfet",
        "comment_body": "Why not make dim a `size_t`? Also, its name shadows method argument, isn't it?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2132818445",
    "pr_number": 155134,
    "pr_file": "c10/cuda/CUDACachingAllocator.h",
    "created_at": "2025-06-06T19:42:54+00:00",
    "commented_code": "MemPool(\n      CUDACachingAllocator::CUDAAllocator* allocator = nullptr,\n      bool is_user_created = true,\n      bool use_on_oom = false);\n      bool use_on_oom = false,\n      bool symm_mem = false);\n  MemPool(const MemPool&) = delete;\n  MemPool(MemPool&&) = default;\n  MemPool& operator=(const MemPool&) = delete;\n  MemPool& operator=(MemPool&&) = default;\n  ~MemPool();\n\n  MempoolId_t id();\n  bool symm_mem();",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2132818445",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 155134,
        "pr_file": "c10/cuda/CUDACachingAllocator.h",
        "discussion_id": "2132818445",
        "commented_code": "@@ -535,14 +535,16 @@ struct C10_CUDA_API MemPool {\n   MemPool(\n       CUDACachingAllocator::CUDAAllocator* allocator = nullptr,\n       bool is_user_created = true,\n-      bool use_on_oom = false);\n+      bool use_on_oom = false,\n+      bool symm_mem = false);\n   MemPool(const MemPool&) = delete;\n   MemPool(MemPool&&) = default;\n   MemPool& operator=(const MemPool&) = delete;\n   MemPool& operator=(MemPool&&) = default;\n   ~MemPool();\n \n   MempoolId_t id();\n+  bool symm_mem();",
        "comment_created_at": "2025-06-06T19:42:54+00:00",
        "comment_author": "kwen2501",
        "comment_body": "nit: `is_symmetric()`?",
        "pr_file_module": null
      },
      {
        "comment_id": "2159858849",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 155134,
        "pr_file": "c10/cuda/CUDACachingAllocator.h",
        "discussion_id": "2132818445",
        "commented_code": "@@ -535,14 +535,16 @@ struct C10_CUDA_API MemPool {\n   MemPool(\n       CUDACachingAllocator::CUDAAllocator* allocator = nullptr,\n       bool is_user_created = true,\n-      bool use_on_oom = false);\n+      bool use_on_oom = false,\n+      bool symm_mem = false);\n   MemPool(const MemPool&) = delete;\n   MemPool(MemPool&&) = default;\n   MemPool& operator=(const MemPool&) = delete;\n   MemPool& operator=(MemPool&&) = default;\n   ~MemPool();\n \n   MempoolId_t id();\n+  bool symm_mem();",
        "comment_created_at": "2025-06-21T04:25:54+00:00",
        "comment_author": "syed-ahmed",
        "comment_body": "Sounds good!",
        "pr_file_module": null
      }
    ]
  }
]
