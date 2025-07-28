---
title: Hardware compatibility patterns
description: Implement proper hardware compatibility patterns when working with different
  GPU backends and AI frameworks. Many AI applications need to support multiple hardware
  platforms (NVIDIA CUDA, AMD ROCm, Intel XPU, Moore Threads, DirectML, ZLUDA) which
  have different capabilities and limitations.
repository: comfyanonymous/ComfyUI
label: AI
language: Python
comments_count: 6
repository_stars: 83726
---

Implement proper hardware compatibility patterns when working with different GPU backends and AI frameworks. Many AI applications need to support multiple hardware platforms (NVIDIA CUDA, AMD ROCm, Intel XPU, Moore Threads, DirectML, ZLUDA) which have different capabilities and limitations.

Key practices:
1. **Device detection and conditional logic**: Check device capabilities before using specific operations
2. **Graceful fallbacks**: Provide alternative implementations when hardware doesn't support certain operations
3. **Import isolation**: Use helper functions to avoid breaking hardware-specific initialization (like CUDA malloc)
4. **Hardware-specific optimizations**: Apply backend-specific settings while maintaining compatibility

Example implementation:
```python
# Device-specific handling with fallbacks
if image.device.type == 'musa':
    # Moore Threads GPU doesn't support bicubic with antialias
    image = image.cpu()
    image = torch.nn.functional.interpolate(image, size=scale_size, mode="bicubic", antialias=True)
    image = image.to('musa')
else:
    image = torch.nn.functional.interpolate(image, size=scale_size, mode="bicubic", antialias=True)

# Hardware detection with specific optimizations
if "[ZLUDA]" in torch_device_name:
    torch.backends.cudnn.enabled = False
    torch.backends.cuda.enable_flash_sdp(False)
    torch.backends.cuda.enable_math_sdp(True)
    torch.backends.cuda.enable_mem_efficient_sdp(False)

# DirectML-specific tensor operations
if comfy.model_management.is_directml_enabled():
    latents_ubyte = latents_ubyte.to(dtype=torch.uint8)
    latents_ubyte = latents_ubyte.to(device="cpu", dtype=torch.uint8, non_blocking=...)
```

This approach ensures AI applications work reliably across different hardware while taking advantage of platform-specific optimizations where available.