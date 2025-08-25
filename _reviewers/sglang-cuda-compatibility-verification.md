---
title: CUDA compatibility verification
description: 'When modifying CUDA versions or GPU architecture configurations in AI/ML
  projects, verify compatibility across three critical dimensions: CUDA version support,
  GPU architecture coverage, and dependent library requirements. Check official compatibility
  matrices, test with target hardware, and validate that AI libraries maintain their
  functionality.'
repository: sgl-project/sglang
label: AI
language: Dockerfile
comments_count: 2
repository_stars: 17245
---

When modifying CUDA versions or GPU architecture configurations in AI/ML projects, verify compatibility across three critical dimensions: CUDA version support, GPU architecture coverage, and dependent library requirements. Check official compatibility matrices, test with target hardware, and validate that AI libraries maintain their functionality.

For GPU architectures, prefer inclusive configurations that support multiple generations rather than restrictive single-architecture builds. For example, use `CMAKE_CUDA_ARCHITECTURES=90;100;120` and `TORCH_CUDA_ARCH_LIST="9.0 10.0 12.0"` to support Hopper and Blackwell families together.

Before upgrading CUDA versions, consult framework release notes (e.g., PyTorch dropped CUDA 12.4 support in v2.7.0) and verify that critical dependencies like specialized AI libraries won't break. Some libraries have strict version requirements that may disable features if not met exactly.

Example verification process:
```dockerfile
# Check base image CUDA version
FROM nvcr.io/nvidia/tritonserver:25.03-py3-min  # Contains CUDA 12.8

# Configure for multiple GPU generations
ARG CMAKE_CUDA_ARCHITECTURES=90;100;120
ARG TORCH_CUDA_ARCH_LIST="9.0 10.0 12.0"

# Validate compatibility with AI dependencies
RUN python -c "import torch; print(f'CUDA: {torch.version.cuda}, Architectures: {torch.cuda.get_arch_list()}')"
```