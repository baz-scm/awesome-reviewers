---
title: Dependency Version Policy
description: 'In configuration files like `requirements.txt`, define a consistent
  versioning policy:


  - Prefer **minimum version constraints** (`>=`) for most libraries to guarantee
  required behavior without freezing to a single patch/release.'
repository: awslabs/agentcore-samples
label: Configurations
language: Txt
comments_count: 4
repository_stars: 3244
---

In configuration files like `requirements.txt`, define a consistent versioning policy:

- Prefer **minimum version constraints** (`>=`) for most libraries to guarantee required behavior without freezing to a single patch/release.
- When you need **reproducible installs** across machines/CI, generate an exact set of transitive dependencies using a compiler/lock workflow (e.g., `uv pip compile`) and commit the resulting `requirements.txt`.
- Use **exact pins** (`==`) only for **specific high-risk/critical integrations** where compatibility must be enforced (then justify and revisit the pin periodically).

Example:
```txt
# Prefer minimum versions
boto3>=1.34.0
langchain_core>=0.3.0

# If compatibility requires it for a specific integration
mcp==1.2.3
```

Example reproducible build flow:
```bash
uv pip compile --output-file requirements.txt pyproject.toml
```

This prevents “works on my machine” drift, avoids breakage from unbounded upgrades, and keeps exceptions tightly scoped to the components that truly require them.