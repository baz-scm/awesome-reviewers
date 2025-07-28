---
title: follow protocol standards
description: When implementing network protocols or communication formats, prioritize
  standardized specifications over legacy or device-specific formats, even when existing
  code uses older approaches. Legacy formats may work but can cause compatibility
  issues and confusion for applications that expect standard compliance.
repository: neovim/neovim
label: Networking
language: C
comments_count: 2
repository_stars: 91433
---

When implementing network protocols or communication formats, prioritize standardized specifications over legacy or device-specific formats, even when existing code uses older approaches. Legacy formats may work but can cause compatibility issues and confusion for applications that expect standard compliance.

For example, when implementing Device Attributes (DA) responses, use the standard format with proper parameter meanings rather than legacy device-specific formats:

```c
// Instead of legacy format that predates standardization:
char vterm_primary_device_attr[] = "1;2;52";  // Device-specific format

// Use standardized format:
char vterm_primary_device_attr[] = "61;52";   // Standard level-1 device with clipboard extension
```

Similarly, ensure protocol detection logic is explicit and follows expected patterns:

```c
// Clear boolean conversion for protocol detection
bool is_tcp = !!strrchr(server_address, ':');
```

This approach improves interoperability, reduces maintenance burden, and ensures your implementation works correctly with a broader range of clients and tools that expect standard-compliant behavior.