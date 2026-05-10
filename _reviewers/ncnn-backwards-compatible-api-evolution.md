---
title: Backwards-Compatible API Evolution
description: When evolving or integrating client-facing interfaces (CLI/API) and platform-dependent
  APIs, preserve compatibility across existing clients and across SDK/platform versions.
repository: Tencent/ncnn
label: API
language: C++
comments_count: 4
repository_stars: 23205
---

When evolving or integrating client-facing interfaces (CLI/API) and platform-dependent APIs, preserve compatibility across existing clients and across SDK/platform versions.

Apply these rules:
1) Backward-compatible interface changes
- If you add an optional parameter, place it at the end so existing positional arguments keep working.

Example (CLI):
```cpp
// Old: prog caffeproto caffemodel ncnnproto ncnnbin quantizelevel int8scaletable
// New: prog ocr|noocr caffeproto caffemodel ncnnproto ncnnbin quantizelevel int8scaletable
// Implementation rule: keep the new optional argument(s) after existing ones, and
// only extend argv parsing in a way that preserves old argc patterns.
```

2) Guard optional platform/API features
- Never assume a flag/enum/symbol exists on every build environment.
- Use feature checks and conditional compilation before setting flags.

Example (Vulkan-like pattern):
```cpp
VkInstanceCreateInfo instanceCreateInfo{};
instanceCreateInfo.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;

// Prefer feature/support-based gating over hard-coding.
if (support_portability_enumeration) {
    instanceCreateInfo.flags |= VK_INSTANCE_CREATE_ENUMERATE_PORTABILITY_BIT_KHR;
}
```

3) Use compatibility shims for missing SDK symbols
- If an enum/definition is missing in older headers, add a controlled header shim (e.g., `vulkan_header_fix.h`) rather than sprinkling ad-hoc defines throughout code.

4) Don’t leak platform/ISA-specific details into stable interfaces
- Keep ISA/rvv-specific parameters (e.g., vector length) resolved inside the implementation instead of being part of the function signature.

Together, these practices keep client interfaces stable for existing users while still allowing safe use of newer platform capabilities.