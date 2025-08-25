---
title: Document AI limitations
description: When implementing AI model support or hardware backends, clearly document
  known limitations, compatibility constraints, and version requirements to prevent
  integration issues and set proper expectations.
repository: sgl-project/sglang
label: AI
language: Markdown
comments_count: 3
repository_stars: 17245
---

When implementing AI model support or hardware backends, clearly document known limitations, compatibility constraints, and version requirements to prevent integration issues and set proper expectations.

AI systems often have specific constraints that can cause runtime failures or unexpected behavior if not properly communicated. This includes quantization limitations, hardware-specific requirements, version dependencies, and feature compatibility matrices.

Key areas to document:
- Model quantization constraints (e.g., "Mixed-bit quantization is not fully supported due to vLLM's layer fusion")
- Hardware backend limitations (e.g., "Wave path only works with page size = 1")
- Version-specific requirements (e.g., "Only python==3.11 is supported currently")
- Performance optimization settings and their rationale

Example documentation pattern:
```markdown
## Known Issues

Several limitations currently affect offline quantized model loading:

1. Mixed-bit Quantization Limitations
   Mixed-bit quantization is not fully supported. Due to vLLM's layer fusion 
   (e.g., QKV fusion), applying different bit-widths to components within the 
   same fused layer can lead to compatibility issues.

2. Limited Support for Quantized MoE Models
   Most quantized MoE models may encounter inference issues due to 
   kernel-related limitations.
```

This prevents users from encountering undocumented failures and helps them choose appropriate alternatives or workarounds.