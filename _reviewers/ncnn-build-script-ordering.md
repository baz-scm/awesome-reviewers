---
title: Build Script Ordering
description: In build/configuration files (e.g., CMakeLists), keep statements organized
  so that they are (1) scoped to the conditions that actually enable the associated
  sources/targets, and (2) ordered deterministically (e.g., alphabetical for registration
  lists).
repository: Tencent/ncnn
label: Code Style
language: Txt
comments_count: 2
repository_stars: 23205
---

In build/configuration files (e.g., CMakeLists), keep statements organized so that they are (1) scoped to the conditions that actually enable the associated sources/targets, and (2) ordered deterministically (e.g., alphabetical for registration lists).

**Apply scope correctly**
- If a source group/entry is only valid when a feature is enabled, place it *inside* the corresponding `if(WITH_...)` block.

**Keep registrations sorted**
- For repeated target/test registrations, sort by name (alphabetical) to reduce review noise and avoid accidental ordering drift.

**Example (CMake)**
```cmake
macro(ncnn_add_layer class)
  foreach(name IN LISTS ${class})
    if(WITH_LAYER_${name})
      if(WITH_LAYER_${name}_${arch})
        # sources only for enabled arch
        source_group("sources\\layers" FILES
          "${CMAKE_CURRENT_SOURCE_DIR}/layer/${name}.cpp")
        source_group("sources\\layers\\${arch}" FILES
          "${CMAKE_CURRENT_SOURCE_DIR}/layer/${arch}/${name}_${arch}.cpp")

        if(WITH_LAYER_${name}_vulkan)
          # sources only for enabled Vulkan
          source_group("sources\\layers\\vulkan" FILES
            "${CMAKE_CURRENT_SOURCE_DIR}/layer/vulkan/${name}_vulkan.cpp")
        endif()
      endif()
    endif()
  endforeach()
endmacro()

# Tests: keep calls alphabetically
ncnn_add_layer_test(AbsVal)
ncnn_add_layer_test(ReLU)
```

This improves readability (future editors can see what is guarded by what) and produces cleaner, more predictable diffs.