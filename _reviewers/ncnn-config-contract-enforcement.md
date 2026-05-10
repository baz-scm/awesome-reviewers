---
title: Config Contract Enforcement
description: When introducing or updating environment/configuration behavior, ensure
  the documented meaning, runtime inputs (CLI/feature flags), and build-time discovery
  (CMake/pkg paths) all point to the same intended target. Avoid “it compiles” success
  that doesn’t enable the feature, and avoid “it builds” that accidentally links against
  a mismatched dependency set.
repository: Tencent/ncnn
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 23205
---

When introducing or updating environment/configuration behavior, ensure the documented meaning, runtime inputs (CLI/feature flags), and build-time discovery (CMake/pkg paths) all point to the same intended target. Avoid “it compiles” success that doesn’t enable the feature, and avoid “it builds” that accidentally links against a mismatched dependency set.

Apply this checklist:
1) Runtime flags must match documentation semantics
- If a config value means “disabled” (e.g., `gpu_device = -1`), do not report results or behavior as if the feature were enabled. Ensure the corresponding benchmark/runtime command-line option actually enables it.

2) Build-time dependency resolution must be anchored to an explicit prefix
- Install dependencies to a dedicated directory via `--prefix`.
- In CMake, set `CMAKE_PREFIX_PATH` to paths under that prefix (so bin/lib/include match) BEFORE `find_package`.

Example (CMake prefix configuration):
```cmake
# e.g., /path/to/protobuf/install
set(ProtobufRoot "/path/to/protobuf/install")

# Point CMake to the exact install root’s artifacts
list(APPEND CMAKE_PREFIX_PATH
     "${ProtobufRoot}/bin"
     "${ProtobufRoot}/lib"
     "${ProtobufRoot}/include")

find_package(Protobuf REQUIRED)
```

If configuration involves both build and runtime, verify end-to-end: the build-time selection (what got found/linked) and the runtime enablement (what got switched on) are consistent with the docs and expected behavior.