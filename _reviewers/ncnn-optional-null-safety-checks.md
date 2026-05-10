---
title: Optional Null Safety Checks
description: When code depends on possibly-missing inputs/outputs or optional attributes,
  do not index or read them unconditionally. Add explicit guards for presence and
  fall back to a safe default/overload.
repository: Tencent/ncnn
label: Null Handling
language: C++
comments_count: 3
repository_stars: 23205
---

When code depends on possibly-missing inputs/outputs or optional attributes, do not index or read them unconditionally. Add explicit guards for presence and fall back to a safe default/overload.

Apply this pattern:
- For vector-based tensors: verify `bottom_blobs.size()` / `top_blobs.size()` before using fixed indices (e.g., hidden/cell), and if hidden/cell aren’t provided, delegate to the simpler overload.
- For operator attributes: verify the attribute exists before reading it (e.g., `n.has_attr("eps")`); only then use the value, otherwise use the intended default.

Example (vector forward fallback):
```cpp
int forward(const std::vector<Mat>& bottom_blobs,
            std::vector<Mat>& top_blobs,
            const Option& opt) const {
    if (bottom_blobs.size() < 1 || top_blobs.size() < 1)
        return -100;

    // hidden/cell optional: only use them when present
    if (top_blobs.size() >= 3) {
        // access indices safely
        Mat& hidden_state = top_blobs[1];
        Mat& cell_state = top_blobs[2];
        return forward(bottom_blobs[0], top_blobs[0], hidden_state, cell_state, opt);
    }

    // safe fallback
    Mat& top_blob = top_blobs[0];
    return forward(bottom_blobs[0], top_blob, opt);
}
```

Example (attribute existence guard):
```cpp
float eps = 1e-3f; // intended default
if (n.has_attr("eps"))
    eps = n.attr("eps");
```

Rule of thumb: if the code would otherwise dereference an index or consume an attribute that may not be present, you must add a guard and a fallback path before the dereference.