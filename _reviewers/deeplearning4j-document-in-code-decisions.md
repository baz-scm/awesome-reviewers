---
title: Document in-code decisions
description: Always include explanations for implementation decisions, non-obvious
  constructs, and specialized functions directly within the code as comments, rather
  than relying on external systems like commit messages or GitHub discussions. This
  practice ensures that future developers can understand the code's purpose and behavior
  without having to search through...
repository: deeplearning4j/deeplearning4j
label: Documentation
language: CUDA
comments_count: 2
repository_stars: 14036
---

Always include explanations for implementation decisions, non-obvious constructs, and specialized functions directly within the code as comments, rather than relying on external systems like commit messages or GitHub discussions. This practice ensures that future developers can understand the code's purpose and behavior without having to search through external documentation.

For example, when using specialized functions or constructs like in this case:

```cpp
// This prepares data for GPU processing by synchronizing host memory to device memory
// and ensures proper buffer handling before computation
NDArray::prepareSpecialUse({ &output }, { &input });

// Implementation code...

// This synchronizes results back from device memory to host memory
NDArray::registerSpecialUse({ &output }, { &input });
```

Similarly, when implementing workarounds or choosing specific implementations:

```cpp
// We default to our custom implementation here because cuDNN has precision issues
// with non-standard padding values and dilated convolutions
return goodType && (input->dataType() == gradO->dataType());
```

This approach makes code more maintainable and reduces onboarding time for new team members who may not have access to historical commit messages or discussions.