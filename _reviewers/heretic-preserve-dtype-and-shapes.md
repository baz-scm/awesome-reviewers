---
title: preserve dtype and shapes
description: When writing PyTorch code, preserve tensor dtypes and devices and be
  explicit about vector/matrix shapes to avoid precision loss, incorrect broadcasting,
  and unnecessary CPU allocations.
repository: p-e-w/heretic
label: Pytorch
language: Python
comments_count: 6
repository_stars: 5002
---

When writing PyTorch code, preserve tensor dtypes and devices and be explicit about vector/matrix shapes to avoid precision loss, incorrect broadcasting, and unnecessary CPU allocations.

Why: mixed-precision and quantized weights are common in model deployment. Unnecessary up/downcasts, implicit device transfers, and incorrect assumptions about 1D tensor shapes (torch treats a 1D tensor as shape (d,) and matmul/outer have specific shape requirements) lead to subtle correctness and performance bugs.

Rules (actionable):
- Do not cast dtypes unless required. If a vector is already float32, avoid .to(torch.float32) again; prefer only changing device: v = v.to(module.weight.device)
- When projecting against possibly low-precision weights, do projection math in a safe compute dtype, but avoid redundant round-trips (downcast then upcast). Example: if refusal_directions is float32 and W is bfloat16/4-bit, move the vector to W's device but keep its dtype:

  # good: preserve dtype, only change device
  v = layer_refusal_direction.to(matrix.device)
  r_transpose_W = torch.matmul(v, matrix)
  matrix.sub_(weight * torch.outer(v, r_transpose_W))

- Be explicit about shapes when using matmul vs outer:
  - Use torch.matmul for vector-matrix products where one operand is 1D (d,) and the other is (d, k). torch.matmul handles (d,) as (1, d) prepended internally.
  - Use torch.outer(a, b) when both a and b are 1D column vectors and you want the full outer product (d, k). Do not pass shaped tensors like (d,1) and (1,k) to torch.outer; prefer 1D tensors.

- Avoid creating tensors on CPU unless necessary. Most torch operations preserve the source device; respect the device of source tensors to prevent implicit transfers and extra memory usage.

- API/type clarity: annotate functions that return modules vs tensors correctly (e.g., dict[str, list[torch.nn.Module]]), and explicitly handle LoRA/quantization lifecycle (attach adapters without unnecessary weight changes; when merging on quantized models, reload base model on CPU and copy adapter weights).

Example (combined pattern):

  # r is (d,) float32 already
  r_device = r.to(matrix.device)
  # r_device: (d,), matrix: (d, k) -> torch.matmul yields (k,)
  r_transpose_W = torch.matmul(r_device, matrix)
  # outer(r, r_transpose_W) -> (d, k)
  matrix.sub_(weight * torch.outer(r_device, r_transpose_W))

Apply these guidelines consistently to avoid unnecessary precision loss, incorrect broadcasting, and extraneous device transfers when working with models, LoRA adapters, and quantized weights.