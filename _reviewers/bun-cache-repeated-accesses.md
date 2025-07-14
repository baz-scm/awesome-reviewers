---
title: Cache repeated accesses
description: When accessing the same property or calling the same function multiple
  times, especially in loops or performance-critical sections, cache the result in
  a local variable. This reduces redundant memory access operations and improves execution
  speed.
repository: oven-sh/bun
label: Performance Optimization
language: C++
comments_count: 2
repository_stars: 79093
---

When accessing the same property or calling the same function multiple times, especially in loops or performance-critical sections, cache the result in a local variable. This reduces redundant memory access operations and improves execution speed.

**Why it matters**: Each property access or function call involves memory lookups and potentially complex operations. Repeating these unnecessarily can significantly impact performance in hot code paths.

**Example - Before optimization:**
```cpp
// Repeated access to nested property in each loop iteration
for (int i = 0; i < sk_X509_num(default_ca_certificates->root_extra_cert_instances); i++) {
  X509 *cert = sk_X509_value(default_ca_certificates->root_extra_cert_instances, i);
  // Use cert...
}
```

**Example - After optimization:**
```cpp
// Cache the property access before the loop
auto instances = default_ca_certificates->root_extra_cert_instances;
for (int i = 0; i < sk_X509_num(instances); i++) {
  X509 *cert = sk_X509_value(instances, i);
  // Use cert...
}
```

This technique is particularly important for:
- Deeply nested property accesses
- Function calls with the same parameters
- Calculations that yield the same result across multiple uses
- Performance-critical loops or hot paths