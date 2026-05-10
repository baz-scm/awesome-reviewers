---
title: Append Only Compatibility
description: When a generated API surface (e.g., an enum/type-id) is derived from
  the order of a registration list, treat that order as part of the public/binary
  API. Never reorder, insert in the middle, or remove/disable entries in that list—add
  new items only by appending at the end.
repository: Tencent/ncnn
label: API
language: Txt
comments_count: 3
repository_stars: 23205
---

When a generated API surface (e.g., an enum/type-id) is derived from the order of a registration list, treat that order as part of the public/binary API. Never reorder, insert in the middle, or remove/disable entries in that list—add new items only by appending at the end.

Example (stable pattern):
```cmake
# Stable ordered list; do not reorder existing entries.
ncnn_add_layer(Reshape)
ncnn_add_layer(ROIPooling)
ncnn_add_layer(Scale)
ncnn_add_layer(Sigmoid)

# New layers must be appended only:
ncnn_add_layer(HardSigmoid)
```

If a change must affect indices (e.g., removing an entry), require an explicit compatibility decision and versioning plan before merging, because it will break existing binaries/serialized models that depend on the numeric ids.