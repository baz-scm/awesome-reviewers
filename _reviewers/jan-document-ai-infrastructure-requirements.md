---
title: Document AI infrastructure requirements
description: When documenting AI applications that run local models or perform inference,
  always provide comprehensive infrastructure requirements including hardware specifications,
  platform-specific drivers, and setup instructions. This ensures users can successfully
  run AI models without encountering compatibility issues.
repository: menloresearch/jan
label: AI
language: Markdown
comments_count: 4
repository_stars: 37620
---

When documenting AI applications that run local models or perform inference, always provide comprehensive infrastructure requirements including hardware specifications, platform-specific drivers, and setup instructions. This ensures users can successfully run AI models without encountering compatibility issues.

Include the following details:
- **Hardware requirements**: Specify RAM/VRAM needs for different model sizes (e.g., "8GB RAM/VRAM for 3B models, 16GB for 7B models")
- **CPU/GPU architecture support**: List supported architectures (ARM, x86 for CPU; NVIDIA, AMD, Intel for GPU)
- **Platform-specific drivers**: Include GPU driver requirements (NVIDIA drivers for Windows, CUDA Toolkit for Linux)
- **Model size relationships**: Explain how hardware capacity relates to usable model sizes

Example documentation structure:
```markdown
### Hardware Requirements
- **RAM/VRAM**: 8GB minimum (3B models), 16GB recommended (7B models)
- **CPU**: ARM, x86 architectures supported
- **GPU**: NVIDIA (via llama.cpp), AMD and Intel support coming soon

### Platform Setup
- **Windows**: Install NVIDIA drivers if GPU available
- **Linux**: Install CUDA Toolkit if GPU available
```

This prevents user frustration and ensures AI applications can run as intended across different hardware configurations.