---
title: HTTP protocol correctness
description: When writing code that touches network addressing or HTTP headers, follow
  the exact protocol semantics rather than relying on convenient shortcuts, since
  subtle deviations break compatibility.
repository: pallets/flask
label: Networking
language: Python
comments_count: 3
repository_stars: 75022
---

When writing code that touches network addressing or HTTP headers, follow the exact protocol semantics rather than relying on convenient shortcuts, since subtle deviations break compatibility.

- Prefer explicit IP addresses over hostnames when binding sockets or servers. A hostname like `localhost` can resolve to either `127.0.0.1` or `::1` depending on the system's DNS/hosts configuration, so it is not a safe drop-in replacement for an explicit address:
  ```python
  # Avoid: relies on OS resolution, may bind to IPv6 instead of IPv4
  host = 'localhost'

  # Prefer: unambiguous
  host = '127.0.0.1'
  ```

- When comparing or searching HTTP header tokens (e.g. `Vary`, cookie names, content-disposition directives), always perform case-insensitive comparisons, since HTTP header field values are case-insensitive per spec:
  ```python
  # Avoid: case-sensitive check can miss existing entries
  if 'Cookie' not in vary_headers:
      ...

  # Prefer: case-insensitive check
  if not any(h.lower() == 'cookie' for h in vary_headers):
      ...
  ```

- When building multi-part header values (e.g. `Content-Disposition` with both `filename` and `filename*`), preserve the order required by the spec/consuming clients instead of relying on dict iteration order or unpacking, since some clients depend on a specific directive order.

Applying these rules prevents hard-to-diagnose networking and HTTP compatibility bugs across different browsers, OS resolvers, and client implementations.