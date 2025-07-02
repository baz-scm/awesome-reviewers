---
title: Optimize device transfers
description: When implementing operations that transfer data between devices (particularly
  CPU to GPU), use device guards and pinned memory to optimize performance. Device
  guards ensure the correct device context, while pinned memory enables asynchronous
  data transfers.
repository: pytorch/pytorch
label: Pytorch
language: Other
comments_count: 5
repository_stars: 91169
---

When implementing operations that transfer data between devices (particularly CPU to GPU), use device guards and pinned memory to optimize performance. Device guards ensure the correct device context, while pinned memory enables asynchronous data transfers.

For device guards, always add them at the beginning of functions that operate on tensors from potentially different devices:
```cpp
// Add device guard based on input tensors
c10::DeviceGuard device_guard(input_t.device());
```

For CPU-to-GPU transfers, use pinned memory to enable non-blocking copies:
```cpp
// When transferring data from CPU to GPU
if (tensor.is_cpu() && destination.device().is_cuda()) {
  // Allocate output in pinned memory for non-blocking transfer
  auto options = tensor.options().pinned_memory(true);
  auto pinned_tensor = at::empty(tensor.sizes(), options);
  // Use pinned tensor as the output or for intermediate operations
  // ...
}
```

Provide clear error messages when operations cannot be performed without copying between devices:
```cpp
TORCH_CHECK(
  !force_move, 
  "cannot move tensor from ", source_device,
  " to ", target_device,
  " without copying. Set copy=True if needed.");
```

These optimizations significantly improve performance by reducing synchronization overhead between CPU and GPU operations.


[
  {
    "discussion_id": "2106417227",
    "pr_number": 154202,
    "pr_file": "aten/src/ATen/native/mkldnn/xpu/Conv.cpp",
    "created_at": "2025-05-26T02:31:41+00:00",
    "commented_code": "return std::tuple<Tensor, Tensor, Tensor>{grad_input, grad_weight, grad_bias};\n}\n\nTensor convolution_pointwise(\n    const Tensor& input_t,\n    const Tensor& weight_t,\n    const std::optional<Tensor>& bias_opt,",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2106417227",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 154202,
        "pr_file": "aten/src/ATen/native/mkldnn/xpu/Conv.cpp",
        "discussion_id": "2106417227",
        "commented_code": "@@ -751,11 +681,134 @@ std::tuple<Tensor, Tensor, Tensor> convolution_backward_overrideable(\n   return std::tuple<Tensor, Tensor, Tensor>{grad_input, grad_weight, grad_bias};\n }\n \n+Tensor convolution_pointwise(\n+    const Tensor& input_t,\n+    const Tensor& weight_t,\n+    const std::optional<Tensor>& bias_opt,",
        "comment_created_at": "2025-05-26T02:31:41+00:00",
        "comment_author": "EikanWang",
        "comment_body": "Pls. add device guard for input tensors and take bias_opt into account.",
        "pr_file_module": null
      },
      {
        "comment_id": "2106656163",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 154202,
        "pr_file": "aten/src/ATen/native/mkldnn/xpu/Conv.cpp",
        "discussion_id": "2106417227",
        "commented_code": "@@ -751,11 +681,134 @@ std::tuple<Tensor, Tensor, Tensor> convolution_backward_overrideable(\n   return std::tuple<Tensor, Tensor, Tensor>{grad_input, grad_weight, grad_bias};\n }\n \n+Tensor convolution_pointwise(\n+    const Tensor& input_t,\n+    const Tensor& weight_t,\n+    const std::optional<Tensor>& bias_opt,",
        "comment_created_at": "2025-05-26T06:38:47+00:00",
        "comment_author": "ZhiweiYan-96",
        "comment_body": "all functions added device guard. \r\n\r\n>>> take bias_opt into account.\r\n\r\nThe device guard should only needs operates on 1 single input, which I refer to the generated files. The reason might be that we only need to change runtime context once.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2155857288",
    "pr_number": 156384,
    "pr_file": "aten/src/ATen/native/IndexingUtils.h",
    "created_at": "2025-06-19T01:50:25+00:00",
    "commented_code": "}\n        // Replace with nonzeros\n        auto nonzero = index.nonzero();\n        if (ensure_same_device && nonzero.device() != self.device()) {\n          bool non_blocking = nonzero.is_cpu() && self.device().is_cuda();",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2155857288",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156384,
        "pr_file": "aten/src/ATen/native/IndexingUtils.h",
        "discussion_id": "2155857288",
        "commented_code": "@@ -39,9 +40,15 @@ static void invalid_mask(const Tensor & self, int64_t idx, const Tensor & mask,\n         }\n         // Replace with nonzeros\n         auto nonzero = index.nonzero();\n+        if (ensure_same_device && nonzero.device() != self.device()) {\n+          bool non_blocking = nonzero.is_cpu() && self.device().is_cuda();",
        "comment_created_at": "2025-06-19T01:50:25+00:00",
        "comment_author": "ngimel",
        "comment_body": "this is not enough to make a copy non-blocking, you also need to copy nonzero to pinned memory",
        "pr_file_module": null
      },
      {
        "comment_id": "2156606565",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156384,
        "pr_file": "aten/src/ATen/native/IndexingUtils.h",
        "discussion_id": "2155857288",
        "commented_code": "@@ -39,9 +40,15 @@ static void invalid_mask(const Tensor & self, int64_t idx, const Tensor & mask,\n         }\n         // Replace with nonzeros\n         auto nonzero = index.nonzero();\n+        if (ensure_same_device && nonzero.device() != self.device()) {\n+          bool non_blocking = nonzero.is_cpu() && self.device().is_cuda();",
        "comment_created_at": "2025-06-19T09:50:53+00:00",
        "comment_author": "lgeiger",
        "comment_body": "Thanks for the fast review. I verified in the pytorch profile that `cudaStreamSynchronize` is not called with this code and `test_sync_warning` also checks that.\r\n\r\nHow would I create a `nonzero` in pinned memory? Can I just create an zero sized empty tensor in pinned memory and use that as the output parameter or is that problematic since we don't know the tensorsize beforehand?\r\n\r\nI'm just asking because I believe simply calling [`nonzero.pin_memory()` is not recommended ](https://docs.pytorch.org/tutorials/intermediate/pinmem_nonblock.html#what-you-will-learn) or is this different here?",
        "pr_file_module": null
      },
      {
        "comment_id": "2160697950",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156384,
        "pr_file": "aten/src/ATen/native/IndexingUtils.h",
        "discussion_id": "2155857288",
        "commented_code": "@@ -39,9 +40,15 @@ static void invalid_mask(const Tensor & self, int64_t idx, const Tensor & mask,\n         }\n         // Replace with nonzeros\n         auto nonzero = index.nonzero();\n+        if (ensure_same_device && nonzero.device() != self.device()) {\n+          bool non_blocking = nonzero.is_cpu() && self.device().is_cuda();",
        "comment_created_at": "2025-06-23T04:35:27+00:00",
        "comment_author": "ngimel",
        "comment_body": "You could allocate zero-element pinned tensor and send it as `out` arg to `nonzero`",
        "pr_file_module": null
      },
      {
        "comment_id": "2161316931",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 156384,
        "pr_file": "aten/src/ATen/native/IndexingUtils.h",
        "discussion_id": "2155857288",
        "commented_code": "@@ -39,9 +40,15 @@ static void invalid_mask(const Tensor & self, int64_t idx, const Tensor & mask,\n         }\n         // Replace with nonzeros\n         auto nonzero = index.nonzero();\n+        if (ensure_same_device && nonzero.device() != self.device()) {\n+          bool non_blocking = nonzero.is_cpu() && self.device().is_cuda();",
        "comment_created_at": "2025-06-23T10:53:24+00:00",
        "comment_author": "lgeiger",
        "comment_body": "@ngimel Done in 0b7acc263f79a11c7f36216b0a620f24969220e8",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2088107795",
    "pr_number": 150218,
    "pr_file": "aten/src/ATen/DLConvertor.cpp",
    "created_at": "2025-05-14T06:03:19+00:00",
    "commented_code": "return fromDLPackImpl<DLManagedTensorVersioned>(src, std::move(deleter));\n}\n\nTensor maybeCopyTensor(\n    const Tensor& data,\n    std::optional<DLDevice> optional_dl_device,\n    std::optional<bool> copy) {\n  bool force_copy = copy.has_value() && *copy;\n  bool force_move = copy.has_value() && !*copy;\n\n  if (optional_dl_device.has_value()) {\n    auto device = at::getATenDevice(\n        optional_dl_device->device_type,\n        static_cast<c10::DeviceIndex>(optional_dl_device->device_id));\n\n    if (device != data.device()) {\n      TORCH_CHECK(\n          !force_move,\n          \"cannot move tensor from \",\n          data.device(),\n          \" to \",\n          device,\n          \" without copying. Set copy=True is needed.\");",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2088107795",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 150218,
        "pr_file": "aten/src/ATen/DLConvertor.cpp",
        "discussion_id": "2088107795",
        "commented_code": "@@ -388,4 +389,35 @@ Tensor fromDLPackVersioned(DLManagedTensorVersioned* src, std::function<void(voi\n   return fromDLPackImpl<DLManagedTensorVersioned>(src, std::move(deleter));\n }\n \n+Tensor maybeCopyTensor(\n+    const Tensor& data,\n+    std::optional<DLDevice> optional_dl_device,\n+    std::optional<bool> copy) {\n+  bool force_copy = copy.has_value() && *copy;\n+  bool force_move = copy.has_value() && !*copy;\n+\n+  if (optional_dl_device.has_value()) {\n+    auto device = at::getATenDevice(\n+        optional_dl_device->device_type,\n+        static_cast<c10::DeviceIndex>(optional_dl_device->device_id));\n+\n+    if (device != data.device()) {\n+      TORCH_CHECK(\n+          !force_move,\n+          \"cannot move tensor from \",\n+          data.device(),\n+          \" to \",\n+          device,\n+          \" without copying. Set copy=True is needed.\");",
        "comment_created_at": "2025-05-14T06:03:19+00:00",
        "comment_author": "msaroufim",
        "comment_body": "just double checking this check would make it clear that users would need to set the copy flag in\r\n\r\n`torch.from_dlpack(..., copy=copy)`",
        "pr_file_module": null
      },
      {
        "comment_id": "2105836795",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 150218,
        "pr_file": "aten/src/ATen/DLConvertor.cpp",
        "discussion_id": "2088107795",
        "commented_code": "@@ -388,4 +389,35 @@ Tensor fromDLPackVersioned(DLManagedTensorVersioned* src, std::function<void(voi\n   return fromDLPackImpl<DLManagedTensorVersioned>(src, std::move(deleter));\n }\n \n+Tensor maybeCopyTensor(\n+    const Tensor& data,\n+    std::optional<DLDevice> optional_dl_device,\n+    std::optional<bool> copy) {\n+  bool force_copy = copy.has_value() && *copy;\n+  bool force_move = copy.has_value() && !*copy;\n+\n+  if (optional_dl_device.has_value()) {\n+    auto device = at::getATenDevice(\n+        optional_dl_device->device_type,\n+        static_cast<c10::DeviceIndex>(optional_dl_device->device_id));\n+\n+    if (device != data.device()) {\n+      TORCH_CHECK(\n+          !force_move,\n+          \"cannot move tensor from \",\n+          data.device(),\n+          \" to \",\n+          device,\n+          \" without copying. Set copy=True is needed.\");",
        "comment_created_at": "2025-05-24T14:18:41+00:00",
        "comment_author": "ysiraichi",
        "comment_body": "Ah, no. Not specifying `copy` should also work, here. Will fix.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2089796566",
    "pr_number": 150218,
    "pr_file": "aten/src/ATen/DLConvertor.cpp",
    "created_at": "2025-05-14T21:42:05+00:00",
    "commented_code": "return fromDLPackImpl<DLManagedTensorVersioned>(src, std::move(deleter));\n}\n\nTensor maybeCopyTensor(\n    const Tensor& data,\n    std::optional<DLDevice> optional_dl_device,\n    std::optional<bool> copy) {\n  bool force_copy = copy.has_value() && *copy;\n  bool force_move = copy.has_value() && !*copy;\n\n  if (optional_dl_device.has_value()) {\n    auto device = at::getATenDevice(\n        optional_dl_device->device_type,\n        static_cast<c10::DeviceIndex>(optional_dl_device->device_id));\n\n    if (device != data.device()) {\n      TORCH_CHECK(\n          !force_move,\n          \"cannot move tensor from \",\n          data.device(),\n          \" to \",\n          device,\n          \" without copying. Set copy=True is needed.\");",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2089796566",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 150218,
        "pr_file": "aten/src/ATen/DLConvertor.cpp",
        "discussion_id": "2089796566",
        "commented_code": "@@ -388,4 +389,35 @@ Tensor fromDLPackVersioned(DLManagedTensorVersioned* src, std::function<void(voi\n   return fromDLPackImpl<DLManagedTensorVersioned>(src, std::move(deleter));\n }\n \n+Tensor maybeCopyTensor(\n+    const Tensor& data,\n+    std::optional<DLDevice> optional_dl_device,\n+    std::optional<bool> copy) {\n+  bool force_copy = copy.has_value() && *copy;\n+  bool force_move = copy.has_value() && !*copy;\n+\n+  if (optional_dl_device.has_value()) {\n+    auto device = at::getATenDevice(\n+        optional_dl_device->device_type,\n+        static_cast<c10::DeviceIndex>(optional_dl_device->device_id));\n+\n+    if (device != data.device()) {\n+      TORCH_CHECK(\n+          !force_move,\n+          \"cannot move tensor from \",\n+          data.device(),\n+          \" to \",\n+          device,\n+          \" without copying. Set copy=True is needed.\");",
        "comment_created_at": "2025-05-14T21:42:05+00:00",
        "comment_author": "albanD",
        "comment_body": "copy=None would also work. It's more that you cannot set copy=False in this case",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2089797023",
    "pr_number": 150218,
    "pr_file": "aten/src/ATen/DLConvertor.cpp",
    "created_at": "2025-05-14T21:42:36+00:00",
    "commented_code": "return fromDLPackImpl<DLManagedTensorVersioned>(src, std::move(deleter));\n}\n\nTensor maybeCopyTensor(\n    const Tensor& data,\n    std::optional<DLDevice> optional_dl_device,\n    std::optional<bool> copy) {\n  bool force_copy = copy.has_value() && *copy;\n  bool force_move = copy.has_value() && !*copy;\n\n  if (optional_dl_device.has_value()) {\n    auto device = at::getATenDevice(\n        optional_dl_device->device_type,\n        static_cast<c10::DeviceIndex>(optional_dl_device->device_id));\n\n    if (device != data.device()) {\n      TORCH_CHECK(\n          !force_move,\n          \"cannot move tensor from \",\n          data.device(),\n          \" to \",\n          device,\n          \" without copying. Set copy=True is needed.\");\n      return data.to(device);\n    }\n  }\n\n  if (force_copy) {\n    return data.detach().clone();",
    "repo_full_name": "pytorch/pytorch",
    "discussion_comments": [
      {
        "comment_id": "2089797023",
        "repo_full_name": "pytorch/pytorch",
        "pr_number": 150218,
        "pr_file": "aten/src/ATen/DLConvertor.cpp",
        "discussion_id": "2089797023",
        "commented_code": "@@ -388,4 +389,35 @@ Tensor fromDLPackVersioned(DLManagedTensorVersioned* src, std::function<void(voi\n   return fromDLPackImpl<DLManagedTensorVersioned>(src, std::move(deleter));\n }\n \n+Tensor maybeCopyTensor(\n+    const Tensor& data,\n+    std::optional<DLDevice> optional_dl_device,\n+    std::optional<bool> copy) {\n+  bool force_copy = copy.has_value() && *copy;\n+  bool force_move = copy.has_value() && !*copy;\n+\n+  if (optional_dl_device.has_value()) {\n+    auto device = at::getATenDevice(\n+        optional_dl_device->device_type,\n+        static_cast<c10::DeviceIndex>(optional_dl_device->device_id));\n+\n+    if (device != data.device()) {\n+      TORCH_CHECK(\n+          !force_move,\n+          \"cannot move tensor from \",\n+          data.device(),\n+          \" to \",\n+          device,\n+          \" without copying. Set copy=True is needed.\");\n+      return data.to(device);\n+    }\n+  }\n+\n+  if (force_copy) {\n+    return data.detach().clone();",
        "comment_created_at": "2025-05-14T21:42:36+00:00",
        "comment_author": "albanD",
        "comment_body": "There should be no autograd here already right? So detach() is not needed",
        "pr_file_module": null
      }
    ]
  }
]
