---
title: API parameter consistency
description: Ensure consistent parameter handling across API methods by using appropriate
  defaults, proper type conversion, validation with meaningful constants, and cross-platform
  behavior consistency.
repository: electron/electron
label: API
language: Other
comments_count: 13
repository_stars: 117644
---

Ensure consistent parameter handling across API methods by using appropriate defaults, proper type conversion, validation with meaningful constants, and cross-platform behavior consistency.

Key practices:
- **Use default parameters** to simplify common use cases: `void SetBounds(const gfx::Rect& bounds, bool animate = false)`
- **Leverage built-in type converters** instead of manual string conversion: `dict.Get("frameOrigin", &frame_origin_url)` where `frame_origin_url` is a `GURL`
- **Use symbolic constants with documentation** for validation: `constexpr int kMinSizeReqdBySpec = 100; // Per Web API spec`
- **Apply consistent validation patterns**: `width = std::max(kMinSizeReqdBySpec, inner_width)`
- **Provide consistent fallback values**: Use "unknown" instead of empty strings for enum-like values
- **Use std::move() for optional parameters**: `SetUserAgent(user_agent, std::move(ua_metadata))`
- **Maintain cross-platform consistency**: Either implement identical behavior across platforms or explicitly gate platform-specific APIs
- **Avoid hardcoded values**: Make configurable what users might want to customize (e.g., animation duration)

This approach reduces API complexity, improves type safety, and ensures predictable behavior across different platforms and use cases.