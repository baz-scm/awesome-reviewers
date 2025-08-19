---
title: Document implementation rationale
description: When implementing networking or system-level functionality where multiple
  approaches exist, always document the rationale behind your implementation choice.
  This is especially critical when the chosen method may not be the most obvious one
  or when platform-specific considerations influence the decision.
repository: ClickHouse/ClickHouse
label: Networking
language: Other
comments_count: 2
repository_stars: 42425
---

When implementing networking or system-level functionality where multiple approaches exist, always document the rationale behind your implementation choice. This is especially critical when the chosen method may not be the most obvious one or when platform-specific considerations influence the decision.

Include relevant documentation excerpts or specifications that support your choice, rather than just providing URLs. Explain why alternative approaches were rejected, particularly regarding reliability, portability, or system compatibility.

Example:
```cpp
/// Unlike s3 and azure, which are object storages,
/// hdfs is a filesystem, so it cannot list files by partial prefix,
/// only by directory.
/// Therefore in the below methods we use allow_partial_prefix=false.
```

This practice prevents future confusion, reduces the likelihood of well-intentioned but incorrect "improvements," and helps maintainers understand the constraints and trade-offs that shaped the implementation. For networking code, this documentation is particularly valuable since different protocols, platforms, and network configurations may require different approaches.