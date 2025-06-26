---
title: "Document feature flags"
description: "When configuring feature flags in Cargo.toml, ensure they are properly structured and documented. Chain feature dependencies correctly, document non-obvious configuration choices with comments, and use appropriate syntax for conditional feature activation."
repository: "tokio-rs/axum"
label: "Configurations"
language: "TOML"
comments_count: 3
repository_stars: 22100
---

When configuring feature flags in Cargo.toml, ensure they are properly structured and documented:

1. **Chain feature dependencies correctly** - Features that depend on other features should explicitly list those dependencies:
```toml
# Incorrect:
cookie-signed = ["cookie-lib/signed"]

# Correct:
cookie-signed = ["cookie", "cookie-lib/signed"]
```

2. **Document non-obvious configuration choices** with comments to help other developers understand your reasoning:
```toml
# `default-features = false` to not depend on tokio which doesn't support compiling to wasm
axum = { path = "../../axum", default-features = false }
```

3. **Use appropriate syntax for conditional feature activation**, understanding special operators like `?` for optional dependencies:
```toml
async-read-body = ["dep:tokio-util", "tokio-util?/io"]
```

These practices ensure that your configuration is both functionally correct and easier for other developers to understand and maintain.