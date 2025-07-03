---
title: Maintain build compatibility
description: When modifying build scripts or configurations, ensure compatibility
  across all supported environments and properly test changes through CI pipelines.
  For tools with version-dependent features, add version checks and provide alternative
  implementations for older versions.
repository: opencv/opencv
label: CI/CD
language: Txt
comments_count: 2
repository_stars: 82865
---

When modifying build scripts or configurations, ensure compatibility across all supported environments and properly test changes through CI pipelines. For tools with version-dependent features, add version checks and provide alternative implementations for older versions.

Example for CMake version-specific features:
```cmake
if(CMAKE_VERSION VERSION_LESS "3.13")
  # Use older approach for CMake < 3.13
  set(PROTOBUF_GENERATE_CPP_APPEND_PATH ON)
  protobuf_generate_cpp(fw_srcs fw_hdrs ${proto_files})
else()
  # Use newer approach available in CMake 3.13+
  protobuf_generate(
    APPEND_PATH
    LANGUAGE cpp
    IMPORT_DIRS ${Protobuf_IMPORT_DIRS}
    OUT_VAR fw_srcs
    PROTOC_EXE ${Protobuf_PROTOC_EXECUTABLE}
    PROTOS ${proto_files})
  # Process the output variables as needed
  set(fw_hdrs "${fw_srcs}")
  list(FILTER fw_srcs EXCLUDE REGEX ".+\.h$")
  list(FILTER fw_hdrs INCLUDE REGEX ".+\.h$")
endif()
```

Always reference the specific CI workflow that validates your build changes (e.g., "This change is tested by the workflow at .github/workflows/OCV-PR-4.x-Android-Test.yaml") to demonstrate the build continues to work across all supported platforms and configurations.
