---
title: Standardize network tools
description: When performing network operations in build scripts or containers, prefer
  `curl` over `wget` for HTTP requests to standardize dependencies and improve portability.
  Use the specific flags `-fsSL` for silent operation with proper error handling,
  and explicitly specify output destinations.
repository: kubeflow/kubeflow
label: Networking
language: Dockerfile
comments_count: 4
repository_stars: 15064
---

When performing network operations in build scripts or containers, prefer `curl` over `wget` for HTTP requests to standardize dependencies and improve portability. Use the specific flags `-fsSL` for silent operation with proper error handling, and explicitly specify output destinations.

Additionally, ensure network services support both IPv4 and IPv6 addressing by using dual-stack binding configurations rather than binding only to 0.0.0.0 (IPv4).

Example replacing wget with curl:
```bash
# Instead of:
wget -q -O- https://example.com/file.tar.gz | tar xz

# Use:
curl -fsSL https://example.com/file.tar.gz | tar xz
```

Example of dual-stack binding in gunicorn:
```bash
# Instead of:
gunicorn -w 3 --bind 0.0.0.0:5000 app:app

# Use:
gunicorn -w 3 --bind 0.0.0.0:5000 --bind [::]:5000 app:app
```
