---
title: Focus documentation content
description: Maintain streamlined primary documentation (like README files) that focuses
  only on currently supported functionality and recommended approaches. Move specialized
  details, legacy systems, or deprecated methods to secondary documentation sources
  like wikis or specialized guides.
repository: fatedier/frp
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 95938
---

Maintain streamlined primary documentation (like README files) that focuses only on currently supported functionality and recommended approaches. Move specialized details, legacy systems, or deprecated methods to secondary documentation sources like wikis or specialized guides.

**Why this matters:**
- Reduces maintenance burden
- Keeps main documentation relevant and concise
- Follows official platform recommendations
- Improves user experience for the majority of users

**Example:**
Instead of:
```markdown
## Installation

### Build from source

- Build with Go >= 1.12
  ```bash
  GO111MODULE=on make
  ```

- Build with Go < 1.12 (Not maintained)
  ```bash
  # Deprecated instructions...
  ```
```

Prefer:
```markdown
## Installation

### Build from source

```bash
GO111MODULE=on make
```

For special build scenarios or legacy systems, please see our [Advanced Build Guide](wiki/advanced-build.md).
```