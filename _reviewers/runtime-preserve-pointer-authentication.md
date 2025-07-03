---
title: Preserve pointer authentication
description: When implementing Pointer Authentication (PAC) for security, maintain
  signed pointers throughout their entire lifecycle to prevent potential security
  vulnerabilities. Avoid unnecessarily stripping PAC signatures from pointers that
  will be stored and later reused. This preserves the security guarantees that PAC
  is designed to provide.
repository: dotnet/runtime
label: Security
language: C++
comments_count: 3
repository_stars: 16578
---

When implementing Pointer Authentication (PAC) for security, maintain signed pointers throughout their entire lifecycle to prevent potential security vulnerabilities. Avoid unnecessarily stripping PAC signatures from pointers that will be stored and later reused. This preserves the security guarantees that PAC is designed to provide.

For example, when storing a return address:

```cpp
// AVOID: Stripping signature before storage creates a security hole
m_pvHJRetAddr = PacStripPtr(m_pvHJRetAddr);

// BETTER: Store the signed pointer to maintain protection
m_pvHJRetAddr = originalSignedPointer;
// Only strip when absolutely necessary for processing
void* strippedForProcessing = PacStripPtr(m_pvHJRetAddr);
```

This approach ensures that any attempt to manipulate the stored address would fail authentication when the pointer is eventually used, significantly reducing the attack surface against return-oriented programming (ROP) attacks. When you do need to strip the signature for processing, limit the scope of the unsigned pointer and avoid storing it in a longer-lived variable or memory location.
