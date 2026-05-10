---
title: Inference Compatibility Rules
description: 'Ensure layer math, parameter semantics, and model conversion/backends
  remain consistent so inference results don’t silently change.


  Apply these rules:'
repository: Tencent/ncnn
label: AI
language: C++
comments_count: 5
repository_stars: 23205
---

Ensure layer math, parameter semantics, and model conversion/backends remain consistent so inference results don’t silently change.

Apply these rules:
- **Backward compatibility:** Do not change default parameter interpretation in a way that alters outputs for existing model files unless you provide a compatibility mechanism (e.g., versioned params) and tests.
- **Convention correctness:** Follow the library’s established conventions for layer parameters (e.g., axis numbering). If multiple frameworks differ, translate explicitly at load/convert time.
- **Numerical correctness:** Implement numerically sensitive formulas exactly (e.g., BatchNorm stability term belongs inside the sqrt when required).
- **Conversion/runtime parity:** Conversion passes must only emit layers/operators that the runtime can execute. If the layer doesn’t exist yet, either implement it now or skip that conversion.
- **Fast-path gating:** If an optimized path (packing/fast mode) isn’t fully implemented, disable it based on the controlling flag and **fall back** to the correct baseline implementation.

Example pattern for fast-path gating:
```cpp
int create_pipeline(const Option& opt) {
    if (opt.fast_gelu == 0) {
        support_packing = false; // disable incomplete fast/packing
    }
    return 0;
}

int forward_inplace(Mat& x, const Option& opt) const {
    if (opt.fast_gelu == 0) {
        // correct baseline implementation
        return GELU::forward(x, opt);
    }
    // otherwise run optimized path
    // ...
    return 0;
}
```

These rules prevent silent output drift across AI inference workloads and keep model conversion reliable.