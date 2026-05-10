---
title: Eliminate Shared Mutable State
description: Ensure concurrent execution is race-free by (a) not storing per-inference
  mutable state in shared layer objects, (b) keeping OpenMP loop temporaries thread-local,
  and (c) using the correct synchronization primitive for the target platform.
repository: Tencent/ncnn
label: Concurrency
language: Other
comments_count: 3
repository_stars: 23205
---

Ensure concurrent execution is race-free by (a) not storing per-inference mutable state in shared layer objects, (b) keeping OpenMP loop temporaries thread-local, and (c) using the correct synchronization primitive for the target platform.

Apply these rules:
1) State must be owned by the running instance, not by the shared model/layer.
- Avoid patterns like `mutable` members updated in `forward()`.
- If an operator needs recurrent state (e.g., LSTM hidden/cell), pass it in via inputs and return updated state via outputs (so separate Extractors don’t race on the same layer object).

Example pattern:
```cpp
// Instead of: mutable Mat hidden, cell; hidden=...; cell=...; in forward()
// Do:
int forward(const std::vector<Blob*>& bottom_blobs,
            std::vector<Blob*>& top_blobs) {
    const Mat& hidden_in = bottom_blobs[HIDDEN_BLOB_INDEX]->data;
    const Mat& cell_in   = bottom_blobs[CELL_BLOB_INDEX]->data;
    Mat hidden_out, cell_out;
    // compute hidden_out/cell_out...
    top_blobs[HIDDEN_OUT]->data = hidden_out;
    top_blobs[CELL_OUT]->data   = cell_out;
    return 0;
}
```

2) In parallel loops, never let per-iteration data become shared state.
- In `#pragma omp parallel for`, any pointer/variable that changes per iteration (e.g., `pc`, `pa`, `scales`, `bias`) must be thread-local or loop-local (declared inside the loop or as private variables), not shared across iterations.

3) Locking primitives must match platform semantics.
- If a mutex/condition-variable implementation differs by OS/toolchain support, use macro guards so the concurrency contract holds on all targets (e.g., XP-compatible `CRITICAL_SECTION` vs newer primitives).