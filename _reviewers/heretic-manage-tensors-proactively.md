---
title: Manage tensors proactively
description: 'Motivation: Large models and matrix ops can produce big ephemeral tensors,
  cross-device copies, and temporary allocations that lead to excessive memory use
  or OOMs. Adopt consistent, device-aware tensor handling, prefer built-in ops, and
  free large temporaries at clear boundaries.'
repository: p-e-w/heretic
label: Performance Optimization
language: Python
comments_count: 8
repository_stars: 5002
---

Motivation: Large models and matrix ops can produce big ephemeral tensors, cross-device copies, and temporary allocations that lead to excessive memory use or OOMs. Adopt consistent, device-aware tensor handling, prefer built-in ops, and free large temporaries at clear boundaries.

Guidelines:
- Avoid unnecessary copies: use Tensor.to(dtype, copy=True) when you need a guaranteed new tensor; skip copying if you don't perform in-place mutation.
  Example: W = base_weight.to(torch.float32, copy=True)  # only if you will modify W in-place

- Use built-in numeric primitives where possible (F.normalize, torch.linalg.vector_norm, etc.) instead of brittle manual clamps. Prefer out= variants if you truly need to avoid temporaries.
  Example: F.normalize(W, p=2, dim=1, out=W)  # in-place normalization to save allocs when safe

- Be device-aware: move small helpers to the target tensor's device before heavy ops to avoid implicit cross-device copies.
  Example: device_projector = projector.to(matrix.device)
           matrix.sub_(weight * (device_projector @ matrix))

- Free large temporaries at well-defined lifecycle boundaries (model reload, merge/save, end of trial). If you observe OOMs or large resident memory, explicitly delete big objects and force collection:
  Example:
    del merged_model
    import gc, torch
    gc.collect()
    torch.cuda.empty_cache()
  Use these only at boundaries where large tensors are no longer needed; don't sprinkle gc.collect() indiscriminately.

- Profile expensive steps (e.g., low-rank SVD) before tuning: measure runtime and only reduce accuracy parameters (q, niter, rank) if they meaningfully affect end-to-end time/quality.

When to use which pattern:
- Small temporary adjustments and pure computations: prefer out-of-place safe ops and avoid premature gc.
- Large model merges, reloads, or per-trial bulk computations: delete large objects promptly and call gc.collect() + torch.cuda.empty_cache() on memory-constrained systems.

Result: following these practices reduces peak/resident memory, avoids hidden cross-device allocations, and keeps heavy numeric code both readable and efficient.