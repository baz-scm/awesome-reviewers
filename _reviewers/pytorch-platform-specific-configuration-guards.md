---
title: Platform-specific configuration guards
description: 'When implementing platform-specific or version-dependent code, use the
  simplest and most maintainable configuration guards. Follow these practices:


  1. **Use the simplest sufficient guard:** If a feature is already gated to a specific
  platform by a build flag, avoid adding redundant architecture checks.'
repository: pytorch/pytorch
label: Configurations
language: Other
comments_count: 5
repository_stars: 91169
---

When implementing platform-specific or version-dependent code, use the simplest and most maintainable configuration guards. Follow these practices:

1. **Use the simplest sufficient guard:** If a feature is already gated to a specific platform by a build flag, avoid adding redundant architecture checks.
   ```cpp
   // Prefer this (if USE_FBGEMM is already x86-specific)
   #ifdef USE_FBGEMM
   // FBGEMM-specific code
   #endif
   
   // Instead of this
   #if defined(USE_FBGEMM) && (defined(__x86_64__) || defined(_M_X64))
   // FBGEMM-specific code
   #endif
   ```

2. **Create helper macros for version checks:** For recurring version-dependent features, define clear helper macros to improve readability.
   ```cpp
   // Define a reusable macro for CUDA version checks
   #if defined(CUDA_VERSION) && CUDA_VERSION >= 12030
   #define IF_CUDA_VERSION_GE_12030(x) x
   #else
   #define IF_CUDA_VERSION_GE_12030(x)
   #endif
   ```

3. **Consider API consistency:** When conditional compilation affects public APIs, prefer implementing the API unconditionally but throwing runtime errors for unavailable features rather than completely omitting the API.
   ```cpp
   // Prefer this (consistent API, runtime check)
   void initVulkanModule(PyObject* module) {
   #ifdef USE_VULKAN
     // Actual implementation
   #else
     throw std::runtime_error("Vulkan support not available");
   #endif
   }
   
   // Instead of conditionally defining the function entirely
   ```

Following these practices ensures your code is more maintainable, provides consistent APIs across different builds, and avoids unnecessary complexity in platform-specific sections.


[
  {
    "discussion_id": "2168294829",
    "pr_number": 156097,
    "pr_file": "c10/cuda/driver_api.h",
    "created_at": "2025-06-26T06:47:56+00:00",
    "commented_code": "}                                                                      \\\n  } while (0)\n\n#define C10_LIBCUDA_DRIVER_API(_)   \\\n  _(cuDeviceGetAttribute)           \\\n  _(cuMemAddressReserve)            \\\n  _(cuMemRelease)                   \\\n  _(cuMemMap)                       \\\n  _(cuMemAddressFree)               \\\n  _(cuMemSetAccess)                 \\\n  _(cuMemUnmap)                     \\\n  _(cuMemCreate)                    \\\n  _(cuMemGetAllocationGranularity)  \\\n  _(cuMemExportToShareableHandle)   \\\n  _(cuMemImportFromShareableHandle) \\\n  _(cuMemsetD32Async)               \\\n  _(cuStreamWriteValue32)           \\\n  _(cuGetErrorString)\n\n#if defined(CUDA_VERSION) && (CUDA_VERSION >= 12030)\n#define C10_LIBCUDA_DRIVER_API_12030(_) \\\n  _(cuMulticastAddDevice)               \\\n  _(cuMulticastBindMem)                 \\\n  _(cuMulticastCreate)\n#if defined(CUDA_VERSION) && CUDA_VERSION >= 12030\n#define IF_CUDA_VERSION_GE_12030(x) x\n#else\n#define C10_LIBCUDA_DRIVER_API_12030(_)\n#define IF_CUDA_VERSION_GE_12030(x)\n#endif\n\n#define C10_LIBCUDA_DRIVER_API(_)                          \\\n  _(cuDeviceGetAttribute, 12000)                           \\\n  _(cuMemAddressReserve, 12000)                            \\\n  _(cuMemRelease, 12000)                                   \\\n  _(cuMemMap, 12000)                                       \\\n  _(cuMemAddressFree, 12000)                               \\\n  _(cuMemSetAccess, 12000)                                 \\\n  _(cuMemUnmap, 12000)                                     \\\n  _(cuMemCreate, 12000)                                    \\\n  _(cuMemGetAllocationGranularity, 12000)                  \\\n  _(cuMemExportToShareableHandle, 12000)                   \\\n  _(cuMemImportFromShareableHandle, 12000)                 \\\n  _(cuMemsetD32Async, 12000)                               \\\n  _(cuStreamWriteValue32, 12000)                           \\\n  _(cuGetErrorString, 12000)                               \\\n  IF_CUDA_VERSION_GE_12030(_(cuMulticastAddDevice, 12030)) \\",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2168294829",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156097,
        "pr_file": "c10/cuda/driver_api.h",
        "discussion_id": "2168294829",
        "commented_code": "@@ -20,31 +20,31 @@\n     }                                                                      \\\n   } while (0)\n \n-#define C10_LIBCUDA_DRIVER_API(_)   \\\n-  _(cuDeviceGetAttribute)           \\\n-  _(cuMemAddressReserve)            \\\n-  _(cuMemRelease)                   \\\n-  _(cuMemMap)                       \\\n-  _(cuMemAddressFree)               \\\n-  _(cuMemSetAccess)                 \\\n-  _(cuMemUnmap)                     \\\n-  _(cuMemCreate)                    \\\n-  _(cuMemGetAllocationGranularity)  \\\n-  _(cuMemExportToShareableHandle)   \\\n-  _(cuMemImportFromShareableHandle) \\\n-  _(cuMemsetD32Async)               \\\n-  _(cuStreamWriteValue32)           \\\n-  _(cuGetErrorString)\n-\n-#if defined(CUDA_VERSION) && (CUDA_VERSION >= 12030)\n-#define C10_LIBCUDA_DRIVER_API_12030(_) \\\n-  _(cuMulticastAddDevice)               \\\n-  _(cuMulticastBindMem)                 \\\n-  _(cuMulticastCreate)\n+#if defined(CUDA_VERSION) && CUDA_VERSION >= 12030\n+#define IF_CUDA_VERSION_GE_12030(x) x\n #else\n-#define C10_LIBCUDA_DRIVER_API_12030(_)\n+#define IF_CUDA_VERSION_GE_12030(x)\n #endif\n \n+#define C10_LIBCUDA_DRIVER_API(_)                          \\\n+  _(cuDeviceGetAttribute, 12000)                           \\\n+  _(cuMemAddressReserve, 12000)                            \\\n+  _(cuMemRelease, 12000)                                   \\\n+  _(cuMemMap, 12000)                                       \\\n+  _(cuMemAddressFree, 12000)                               \\\n+  _(cuMemSetAccess, 12000)                                 \\\n+  _(cuMemUnmap, 12000)                                     \\\n+  _(cuMemCreate, 12000)                                    \\\n+  _(cuMemGetAllocationGranularity, 12000)                  \\\n+  _(cuMemExportToShareableHandle, 12000)                   \\\n+  _(cuMemImportFromShareableHandle, 12000)                 \\\n+  _(cuMemsetD32Async, 12000)                               \\\n+  _(cuStreamWriteValue32, 12000)                           \\\n+  _(cuGetErrorString, 12000)                               \\\n+  IF_CUDA_VERSION_GE_12030(_(cuMulticastAddDevice, 12030)) \\",
        "comment_created_at": "2025-06-26T06:47:56+00:00",
        "comment_author": "wujingyue",
        "comment_body": "```suggestion\r\n  _(cuMulticastAddDevice, 12030) \\\r\n```\r\nWhat you wrote is totally fine. \r\n\r\nI'd make it less verbose. If the CUDA driver is older than 12.3 (or 12.1 as you said), cuMulticastAddDevice will fail [this assertion](https://github.com/pytorch/pytorch/blob/50b2069b61942e923528c94ccbbc8ab5e92c381e/c10/cuda/driver_api.cpp#L19). An assertion error is harder to discover than a compile-time error, but I tend to find it OK in practice. ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2151477389",
    "pr_number": 156161,
    "pr_file": "aten/src/ATen/native/cpu/ScatterGatherKernel.cpp",
    "created_at": "2025-06-17T07:00:14+00:00",
    "commented_code": "int64_t* sorted_col_index_keys = nullptr;\n  int64_t* sorted_col_index_values = nullptr;\n  \n#if defined(USE_FBGEMM) && (defined(__x86_64__) || defined(_M_X64))",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2151477389",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156161,
        "pr_file": "aten/src/ATen/native/cpu/ScatterGatherKernel.cpp",
        "discussion_id": "2151477389",
        "commented_code": "@@ -719,13 +939,24 @@ void cpu_scatter_reduce_expanded_index(const Tensor& self, const Tensor& index,\n \n   int64_t* sorted_col_index_keys = nullptr;\n   int64_t* sorted_col_index_values = nullptr;\n+  \n+#if defined(USE_FBGEMM) && (defined(__x86_64__) || defined(_M_X64))",
        "comment_created_at": "2025-06-17T07:00:14+00:00",
        "comment_author": "fadara01",
        "comment_body": "why is `#if defined(USE_FBGEMM)` not enough?",
        "pr_file_module": null
      },
      {
        "comment_id": "2163038637",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156161,
        "pr_file": "aten/src/ATen/native/cpu/ScatterGatherKernel.cpp",
        "discussion_id": "2151477389",
        "commented_code": "@@ -719,13 +939,24 @@ void cpu_scatter_reduce_expanded_index(const Tensor& self, const Tensor& index,\n \n   int64_t* sorted_col_index_keys = nullptr;\n   int64_t* sorted_col_index_values = nullptr;\n+  \n+#if defined(USE_FBGEMM) && (defined(__x86_64__) || defined(_M_X64))",
        "comment_created_at": "2025-06-24T06:07:56+00:00",
        "comment_author": "maajidkhann",
        "comment_body": "Right now, USE_FBGEMM is gated to x86 platforms. So checking just #ifdef USE_FBGEMM is sufficient and simpler.\r\nI was defensively guarding against a potential misconfiguration like - USE_FBGEMM being defined on ARM accidentally.\r\n\r\nAnyways, build system is well-behaved in pytorch, so updated the logic to just  #ifdef USE_FBGEMM",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2164495759",
    "pr_number": 156097,
    "pr_file": "c10/cuda/driver_api.cpp",
    "created_at": "2025-06-24T16:57:18+00:00",
    "commented_code": "return &singleton;\n}\n\nvoid* get_symbol(const char* name) {\n  int runtime_ver = 0, driver_ver = 0;\n  C10_CUDA_CHECK(cudaRuntimeGetVersion(&runtime_ver));\n  C10_CUDA_CHECK(cudaDriverGetVersion(&driver_ver));\n\n  void* out = nullptr;\n  cudaDriverEntryPointQueryResult qres{};\n  if (auto st = cudaGetDriverEntryPoint(name, &out, cudaEnableDefault, &qres);\n      st == cudaSuccess && qres == cudaDriverEntryPointSuccess && out) {\n    return out;\n  }\n\n  unsigned int req_ver = std::min(runtime_ver, driver_ver);\n  if (auto st = cudaGetDriverEntryPointByVersion(",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2164495759",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156097,
        "pr_file": "c10/cuda/driver_api.cpp",
        "discussion_id": "2164495759",
        "commented_code": "@@ -47,6 +43,32 @@ C10_EXPORT DriverAPI* DriverAPI::get() {\n   return &singleton;\n }\n \n+void* get_symbol(const char* name) {\n+  int runtime_ver = 0, driver_ver = 0;\n+  C10_CUDA_CHECK(cudaRuntimeGetVersion(&runtime_ver));\n+  C10_CUDA_CHECK(cudaDriverGetVersion(&driver_ver));\n+\n+  void* out = nullptr;\n+  cudaDriverEntryPointQueryResult qres{};\n+  if (auto st = cudaGetDriverEntryPoint(name, &out, cudaEnableDefault, &qres);\n+      st == cudaSuccess && qres == cudaDriverEntryPointSuccess && out) {\n+    return out;\n+  }\n+\n+  unsigned int req_ver = std::min(runtime_ver, driver_ver);\n+  if (auto st = cudaGetDriverEntryPointByVersion(",
        "comment_created_at": "2025-06-24T16:57:18+00:00",
        "comment_author": "ngimel",
        "comment_body": "in which runtime version was cudaGetDriverEntryPointByVersion added?",
        "pr_file_module": null
      },
      {
        "comment_id": "2165192255",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156097,
        "pr_file": "c10/cuda/driver_api.cpp",
        "discussion_id": "2164495759",
        "commented_code": "@@ -47,6 +43,32 @@ C10_EXPORT DriverAPI* DriverAPI::get() {\n   return &singleton;\n }\n \n+void* get_symbol(const char* name) {\n+  int runtime_ver = 0, driver_ver = 0;\n+  C10_CUDA_CHECK(cudaRuntimeGetVersion(&runtime_ver));\n+  C10_CUDA_CHECK(cudaDriverGetVersion(&driver_ver));\n+\n+  void* out = nullptr;\n+  cudaDriverEntryPointQueryResult qres{};\n+  if (auto st = cudaGetDriverEntryPoint(name, &out, cudaEnableDefault, &qres);\n+      st == cudaSuccess && qres == cudaDriverEntryPointSuccess && out) {\n+    return out;\n+  }\n+\n+  unsigned int req_ver = std::min(runtime_ver, driver_ver);\n+  if (auto st = cudaGetDriverEntryPointByVersion(",
        "comment_created_at": "2025-06-25T00:23:01+00:00",
        "comment_author": "syed-ahmed",
        "comment_body": "Per https://github.com/NVIDIA/cutlass/pull/2086, it was added in 12.5",
        "pr_file_module": null
      },
      {
        "comment_id": "2165209310",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156097,
        "pr_file": "c10/cuda/driver_api.cpp",
        "discussion_id": "2164495759",
        "commented_code": "@@ -47,6 +43,32 @@ C10_EXPORT DriverAPI* DriverAPI::get() {\n   return &singleton;\n }\n \n+void* get_symbol(const char* name) {\n+  int runtime_ver = 0, driver_ver = 0;\n+  C10_CUDA_CHECK(cudaRuntimeGetVersion(&runtime_ver));\n+  C10_CUDA_CHECK(cudaDriverGetVersion(&driver_ver));\n+\n+  void* out = nullptr;\n+  cudaDriverEntryPointQueryResult qres{};\n+  if (auto st = cudaGetDriverEntryPoint(name, &out, cudaEnableDefault, &qres);\n+      st == cudaSuccess && qres == cudaDriverEntryPointSuccess && out) {\n+    return out;\n+  }\n+\n+  unsigned int req_ver = std::min(runtime_ver, driver_ver);\n+  if (auto st = cudaGetDriverEntryPointByVersion(",
        "comment_created_at": "2025-06-25T00:39:14+00:00",
        "comment_author": "syed-ahmed",
        "comment_body": "Yes indeed it was added in 12.5.\r\n12.5: https://docs.nvidia.com/cuda/archive/12.5.0/cuda-runtime-api/group__CUDART__DRIVER__ENTRY__POINT.html#group__CUDART__DRIVER__ENTRY__POINT_1gcf55d143722ccfa9252758181701c876\r\n12.4: https://docs.nvidia.com/cuda/archive/12.4.1/cuda-runtime-api/group__CUDART__DRIVER__ENTRY__POINT.html#group__CUDART__DRIVER__ENTRY__POINT_1gcf55d143722ccfa9252758181701c876",
        "pr_file_module": null
      },
      {
        "comment_id": "2165268430",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156097,
        "pr_file": "c10/cuda/driver_api.cpp",
        "discussion_id": "2164495759",
        "commented_code": "@@ -47,6 +43,32 @@ C10_EXPORT DriverAPI* DriverAPI::get() {\n   return &singleton;\n }\n \n+void* get_symbol(const char* name) {\n+  int runtime_ver = 0, driver_ver = 0;\n+  C10_CUDA_CHECK(cudaRuntimeGetVersion(&runtime_ver));\n+  C10_CUDA_CHECK(cudaDriverGetVersion(&driver_ver));\n+\n+  void* out = nullptr;\n+  cudaDriverEntryPointQueryResult qres{};\n+  if (auto st = cudaGetDriverEntryPoint(name, &out, cudaEnableDefault, &qres);\n+      st == cudaSuccess && qres == cudaDriverEntryPointSuccess && out) {\n+    return out;\n+  }\n+\n+  unsigned int req_ver = std::min(runtime_ver, driver_ver);\n+  if (auto st = cudaGetDriverEntryPointByVersion(",
        "comment_created_at": "2025-06-25T01:42:51+00:00",
        "comment_author": "ngimel",
        "comment_body": "So this needs to be guarded on cuda version? We don't have 12.4 builds in CI (they will be reintroduced soon), but internally we do, and this will be a build error. ",
        "pr_file_module": null
      },
      {
        "comment_id": "2165277453",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156097,
        "pr_file": "c10/cuda/driver_api.cpp",
        "discussion_id": "2164495759",
        "commented_code": "@@ -47,6 +43,32 @@ C10_EXPORT DriverAPI* DriverAPI::get() {\n   return &singleton;\n }\n \n+void* get_symbol(const char* name) {\n+  int runtime_ver = 0, driver_ver = 0;\n+  C10_CUDA_CHECK(cudaRuntimeGetVersion(&runtime_ver));\n+  C10_CUDA_CHECK(cudaDriverGetVersion(&driver_ver));\n+\n+  void* out = nullptr;\n+  cudaDriverEntryPointQueryResult qres{};\n+  if (auto st = cudaGetDriverEntryPoint(name, &out, cudaEnableDefault, &qres);\n+      st == cudaSuccess && qres == cudaDriverEntryPointSuccess && out) {\n+    return out;\n+  }\n+\n+  unsigned int req_ver = std::min(runtime_ver, driver_ver);\n+  if (auto st = cudaGetDriverEntryPointByVersion(",
        "comment_created_at": "2025-06-25T01:54:24+00:00",
        "comment_author": "eee4017",
        "comment_body": "OK, I think cudaGetDriverEntryPoint is available starting from 11.3. Do we need to worry about supporting versions earlier than 11.3 ? https://docs.nvidia.com/cuda/archive/11.3.0/cuda-toolkit-release-notes/index.html#cuda-general-new-features",
        "pr_file_module": null
      },
      {
        "comment_id": "2165592482",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156097,
        "pr_file": "c10/cuda/driver_api.cpp",
        "discussion_id": "2164495759",
        "commented_code": "@@ -47,6 +43,32 @@ C10_EXPORT DriverAPI* DriverAPI::get() {\n   return &singleton;\n }\n \n+void* get_symbol(const char* name) {\n+  int runtime_ver = 0, driver_ver = 0;\n+  C10_CUDA_CHECK(cudaRuntimeGetVersion(&runtime_ver));\n+  C10_CUDA_CHECK(cudaDriverGetVersion(&driver_ver));\n+\n+  void* out = nullptr;\n+  cudaDriverEntryPointQueryResult qres{};\n+  if (auto st = cudaGetDriverEntryPoint(name, &out, cudaEnableDefault, &qres);\n+      st == cudaSuccess && qres == cudaDriverEntryPointSuccess && out) {\n+    return out;\n+  }\n+\n+  unsigned int req_ver = std::min(runtime_ver, driver_ver);\n+  if (auto st = cudaGetDriverEntryPointByVersion(",
        "comment_created_at": "2025-06-25T03:42:54+00:00",
        "comment_author": "ngimel",
        "comment_body": "No, 12.0 is the earliest version we suppot",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2098997916",
    "pr_number": 153991,
    "pr_file": "torch/csrc/Module.cpp",
    "created_at": "2025-05-20T23:01:15+00:00",
    "commented_code": "#ifdef USE_MPS\n  torch::mps::initModule(module);\n#endif\n#ifdef USE_VULKAN",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2098997916",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 153991,
        "pr_file": "torch/csrc/Module.cpp",
        "discussion_id": "2098997916",
        "commented_code": "@@ -1891,6 +1892,9 @@ PyObject* initModule() {\n #ifdef USE_MPS\n   torch::mps::initModule(module);\n #endif\n+#ifdef USE_VULKAN",
        "comment_created_at": "2025-05-20T23:01:15+00:00",
        "comment_author": "albanD",
        "comment_body": "Can we do this ifdef insite the initModule?\r\nThis is a footgun where it becomes very easy to define APIs that exist or not on the python module depending on build flags.\r\nThis is a big issue for distributed that does that today as anyone that \"import\" your function in python will see their script crash in a weird way with another install of PyTorch. And catching these import errors is hard.\r\n\r\nIt is best if we could have always the same API but it throws an error if you try to use it.",
        "pr_file_module": null
      },
      {
        "comment_id": "2099013258",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 153991,
        "pr_file": "torch/csrc/Module.cpp",
        "discussion_id": "2098997916",
        "commented_code": "@@ -1891,6 +1892,9 @@ PyObject* initModule() {\n #ifdef USE_MPS\n   torch::mps::initModule(module);\n #endif\n+#ifdef USE_VULKAN",
        "comment_created_at": "2025-05-20T23:15:42+00:00",
        "comment_author": "swolchok",
        "comment_body": "I tried to make this match MPS, which is directly above. I take it this is a case where it's too late to fix MPS but not Vulkan?",
        "pr_file_module": null
      },
      {
        "comment_id": "2099067993",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 153991,
        "pr_file": "torch/csrc/Module.cpp",
        "discussion_id": "2098997916",
        "commented_code": "@@ -1891,6 +1892,9 @@ PyObject* initModule() {\n #ifdef USE_MPS\n   torch::mps::initModule(module);\n #endif\n+#ifdef USE_VULKAN",
        "comment_created_at": "2025-05-21T00:15:19+00:00",
        "comment_author": "albanD",
        "comment_body": "Correct! :) ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2029450813",
    "pr_number": 150705,
    "pr_file": "aten/src/ATen/native/cuda/MemoryAccess.cuh",
    "created_at": "2025-04-04T21:21:23+00:00",
    "commented_code": "uint64_t address = reinterpret_cast<uint64_t>(pointer);\n  constexpr int vec2_alignment = std::alignment_of_v<aligned_vector<scalar_t, 2>>;\n  constexpr int vec4_alignment = std::alignment_of_v<aligned_vector<scalar_t, 4>>;\n#if defined(USE_ROCM) || (defined(CUDA_VERSION) && CUDA_VERSION >= 12080)",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2029450813",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 150705,
        "pr_file": "aten/src/ATen/native/cuda/MemoryAccess.cuh",
        "discussion_id": "2029450813",
        "commented_code": "@@ -486,7 +486,9 @@ inline C10_HOST_DEVICE int can_vectorize_up_to(const char *pointer) {\n   uint64_t address = reinterpret_cast<uint64_t>(pointer);\n   constexpr int vec2_alignment = std::alignment_of_v<aligned_vector<scalar_t, 2>>;\n   constexpr int vec4_alignment = std::alignment_of_v<aligned_vector<scalar_t, 4>>;\n+#if defined(USE_ROCM) || (defined(CUDA_VERSION) && CUDA_VERSION >= 12080)",
        "comment_created_at": "2025-04-04T21:21:23+00:00",
        "comment_author": "eqy",
        "comment_body": "should `USE_ROCM` here also be inverted if the `CUDA_VERSION` condition is `>= 12080`",
        "pr_file_module": null
      },
      {
        "comment_id": "2029462805",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 150705,
        "pr_file": "aten/src/ATen/native/cuda/MemoryAccess.cuh",
        "discussion_id": "2029450813",
        "commented_code": "@@ -486,7 +486,9 @@ inline C10_HOST_DEVICE int can_vectorize_up_to(const char *pointer) {\n   uint64_t address = reinterpret_cast<uint64_t>(pointer);\n   constexpr int vec2_alignment = std::alignment_of_v<aligned_vector<scalar_t, 2>>;\n   constexpr int vec4_alignment = std::alignment_of_v<aligned_vector<scalar_t, 4>>;\n+#if defined(USE_ROCM) || (defined(CUDA_VERSION) && CUDA_VERSION >= 12080)",
        "comment_created_at": "2025-04-04T21:34:33+00:00",
        "comment_author": "malfet",
        "comment_body": "No, I don't think so. Before https://github.com/pytorch/pytorch/pull/145746 vec8_alignment were only available to `USE_ROCM`, after it was enabled unconditionally and I want it to be enabled for either ROCM or CUDA newer than 12.6",
        "pr_file_module": null
      }
    ]
  }
]
