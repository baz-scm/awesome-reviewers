---
title: Check feature compatibility
description: When using kernel-specific networking features like io_uring, always
  implement runtime detection of feature support before enabling them. This ensures
  your code remains compatible across different kernel versions while taking advantage
  of newer optimizations when available.
repository: netty/netty
label: Networking
language: C
comments_count: 2
repository_stars: 34227
---

When using kernel-specific networking features like io_uring, always implement runtime detection of feature support before enabling them. This ensures your code remains compatible across different kernel versions while taking advantage of newer optimizations when available.

For Linux kernel features, verify the minimum required version and implement conditional feature activation. This prevents runtime errors (like EINVAL) on systems with older kernels that don't support specific features.

Example implementation:

```c
struct io_uring_params p;
memset(&p, 0, sizeof(p));

// Check for feature support before enabling
#ifdef IORING_SETUP_SUBMIT_ALL
    // Introduced in kernel 5.18, don't blindly enable
    if (kernel_supports_feature(FEATURE_IORING_SETUP_SUBMIT_ALL)) {
        p.flags |= IORING_SETUP_SUBMIT_ALL;
    }
#endif

#ifdef IORING_SETUP_R_DISABLED
    // Introduced in kernel 6.1, check before using
    if (kernel_supports_feature(FEATURE_IORING_SETUP_R_DISABLED)) {
        p.flags |= IORING_SETUP_R_DISABLED;
    }
#endif
```

Documentation should clearly state which kernel versions are required for specific features. Consider exposing feature detection capabilities to higher-level code so callers can make informed decisions about available functionality.