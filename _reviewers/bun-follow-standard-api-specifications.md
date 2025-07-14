---
title: Follow standard API specifications
description: Ensure API implementations strictly adhere to published specifications,
  even when adding features or optimizations. Deviating from standard behavior can
  create compatibility issues with other implementations (like Node.js) that rely
  on specification-compliant behavior.
repository: oven-sh/bun
label: API
language: C++
comments_count: 2
repository_stars: 79093
---

Ensure API implementations strictly adhere to published specifications, even when adding features or optimizations. Deviating from standard behavior can create compatibility issues with other implementations (like Node.js) that rely on specification-compliant behavior.

When implementing web APIs:
1. Refer directly to official specifications (WHATWG, W3C, ECMAScript) rather than copying other implementations
2. Keep compatibility layers clearly separated from core spec implementation
3. Document any intentional behavior differences

**Example:**
```cpp
// INCORRECT: Adding non-standard behavior directly in core API implementation
void MessagePort::transfer() {
    // This behavior differs from spec - ports shouldn't be "closed" on transfer
    dispatchCloseEvent();
}

// CORRECT: Follow specification behavior
void MessagePort::transfer() {
    detachWithoutClosing(); // Aligns with spec: port is detached but not closed
}

// Alternative for compatibility needs
namespace CompatLayer {
    void handleMessagePortTransfer(MessagePort* port) {
        // Add Node.js specific behavior here if needed
    }
}
```