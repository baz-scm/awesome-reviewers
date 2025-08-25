---
title: Verify AI library compatibility
description: When specifying AI/ML library dependencies, ensure version compatibility
  between related packages and verify that prebuilt binaries are available for the
  target environment. Many AI libraries like auto_gptq, autoawq, and flash_attn are
  compiled against specific versions of PyTorch and CUDA, and version mismatches can
  force compilation from source or cause...
repository: QwenLM/Qwen3
label: AI
language: Txt
comments_count: 3
repository_stars: 24226
---

When specifying AI/ML library dependencies, ensure version compatibility between related packages and verify that prebuilt binaries are available for the target environment. Many AI libraries like auto_gptq, autoawq, and flash_attn are compiled against specific versions of PyTorch and CUDA, and version mismatches can force compilation from source or cause runtime failures.

Before finalizing requirements, check:
- Library compatibility matrices (e.g., auto_gptq 0.7.1 requires torch 2.2.1, not 2.3.1)
- Availability of prebuilt wheels for your CUDA version
- Whether dependencies require CUDA compilers if building from source

Consider separating incompatible libraries into different requirements files when necessary.

Example of problematic dependencies:
```
torch==2.3.1
auto_gptq==0.7.1  # Compiled against torch 2.2.1, will cause issues
```

Better approach:
```
# requirements-gptq.txt
torch==2.2.1
auto_gptq==0.7.1

# requirements-awq.txt  
torch==2.4.1
autoawq==0.2.6
```