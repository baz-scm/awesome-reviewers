---
title: AI library version compatibility
description: When documenting AI/ML model deployment and inference procedures, always
  test and specify compatible library versions to prevent runtime failures. Version
  incompatibilities in AI libraries can cause critical errors like inference failures,
  probability tensor issues, or model output corruption.
repository: QwenLM/Qwen3
label: AI
language: Other
comments_count: 2
repository_stars: 24226
---

When documenting AI/ML model deployment and inference procedures, always test and specify compatible library versions to prevent runtime failures. Version incompatibilities in AI libraries can cause critical errors like inference failures, probability tensor issues, or model output corruption.

Key practices:
- Test all documented version combinations before publication
- Specify exact working versions when known incompatibilities exist
- Document alternative versions when primary versions fail
- Include version-specific notes for critical functionality

Example from model deployment documentation:
```bash
# Working configuration
auto_gptq==0.6.0+cu1210  # Note: >=0.7.0 causes RuntimeError with probability tensors

# vLLM version notes
vLLM==0.6.2  # Recommended for Qwen2.5 7B/14B/32B with 128k context
vLLM==0.6.3  # May cause output issues: !!!!!!!!!!!!!!!!!!!!!!!
```

This prevents users from encountering runtime errors like "probability tensor contains either `inf`, `nan` or element < 0" or model output corruption, ensuring reliable AI model deployment and inference.