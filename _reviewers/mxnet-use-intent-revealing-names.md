---
title: Use intent-revealing names
description: Choose names that clearly reveal the purpose, behavior, or type of the
  code elements they represent. A good name should answer "what" rather than "how"
  and should be precise enough to avoid ambiguity.
repository: apache/mxnet
label: Naming Conventions
language: Other
comments_count: 5
repository_stars: 20801
---

Choose names that clearly reveal the purpose, behavior, or type of the code elements they represent. A good name should answer "what" rather than "how" and should be precise enough to avoid ambiguity.

For functions, choose names that indicate what they do or return:
```cpp
// Less clear
inline bool is_float(const int dtype) {
    // checks if dtype is any floating point type
}

// More clear
inline bool is_floating(const int dtype) {
    // clearly indicates checking for any floating point type
}
```

For variables, use domain-specific terms that express their meaning:
```cpp
// Less clear
const int strides_1 = floor((IH << 1) / OH) - floor(IH / OH);
const int strides_2 = floor((IW << 1) / OW) - floor(IW / OW);

// More clear
const int strides_H = floor((IH << 1) / OH) - floor(IH / OH);
const int strides_W = floor((IW << 1) / OW) - floor(IW / OW);
```

Use prefixes or qualifiers when name conflicts might occur:
```cpp
// Potential conflict with mshadow::kInt8
enum QuantizeOutType { qAuto = 0, qInt8, qUint8 };
```

For configuration variables, be specific about what they control:
```cpp
// Too generic
bool disable_fuse_all = dmlc::GetEnv("MXNET_DISABLE_ONEDNN_FUSE_ALL", false);

// More specific
bool disable_fuse_requantize = dmlc::GetEnv("MXNET_DISABLE_ONEDNN_FUSE_REQUANTIZE", false);
bool disable_fuse_dequantize = dmlc::GetEnv("MXNET_DISABLE_ONEDNN_FUSE_DEQUANTIZE", false);
```

Extract meaningful operations into well-named functions instead of using inline code blocks.
