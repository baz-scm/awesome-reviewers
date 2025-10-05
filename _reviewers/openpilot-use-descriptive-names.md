---
title: Use descriptive names
description: Choose names that clearly communicate purpose and meaning rather than
  using abbreviations or unclear terms. Names should be self-documenting and make
  the code's intent obvious without requiring additional context.
repository: commaai/openpilot
label: Naming Conventions
language: Other
comments_count: 4
repository_stars: 58214
---

Choose names that clearly communicate purpose and meaning rather than using abbreviations or unclear terms. Names should be self-documenting and make the code's intent obvious without requiring additional context.

Avoid abbreviations that obscure meaning. Instead of `ds` use `downscale`, instead of `audioData` and `microphone` use `rawAudio` and `audioMetadata` to clarify their distinct purposes.

Replace computed expressions with semantic variable names. Instead of repeatedly using `width / scale`, define clear variables like `inputSize` and `outputSize`.

Make struct and class names descriptive of their actual purpose. Instead of generic names like `SmolModelDataV2`, use specific names like `DrivingModelData` that indicate what the data represents.

Example:
```cpp
// Poor naming - unclear purpose
void OS04C10::OS04C10_IFE_ds_override() { ... }
struct SmolModelDataV2 { ... }

// Better naming - clear and descriptive  
void OS04C10::ife_downscale_configure() { ... }
struct DrivingModelData { ... }
```

This approach makes code more maintainable and reduces the need for developers to reference other files or documentation to understand what identifiers represent.