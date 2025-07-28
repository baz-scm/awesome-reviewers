---
title: specify network protocol endianness
description: Always explicitly specify byte order (endianness) in network protocol
  documentation and implementations. Even when a specification mandates a particular
  endianness, make it clear in your documentation to avoid confusion and implementation
  errors.
repository: llvm/llvm-project
label: Networking
language: Markdown
comments_count: 2
repository_stars: 33702
---

Always explicitly specify byte order (endianness) in network protocol documentation and implementations. Even when a specification mandates a particular endianness, make it clear in your documentation to avoid confusion and implementation errors.

When documenting network protocols, include explicit statements about byte ordering, especially when the protocol endianness might differ from the host system's native endianness. This prevents ambiguity and helps developers implement the protocol correctly.

Example from qWasmCallStack documentation:
```
Get the Wasm callback for the given thread id. This returns a hex-encoding list
of 64-bit addresses for the frame PCs. To match the Wasm specification, the
addresses are encoded in little endian byte order, even if the endian of the 
Wasm runtime's host is not little endian.
```

This approach eliminates confusion about data representation and ensures consistent implementation across different platforms and architectures.