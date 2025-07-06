---
title: Use structured model metadata
description: Represent AI model information using structured data rather than hardcoded
  enumerations or conditionals. Store capabilities, limitations, and features as structured
  fields that can be queried at runtime. This approach simplifies adding new models,
  detecting feature support, and adapting to model updates without requiring extensive
  code changes.
repository: zed-industries/zed
label: AI
language: Rust
comments_count: 5
repository_stars: 62119
---

Represent AI model information using structured data rather than hardcoded enumerations or conditionals. Store capabilities, limitations, and features as structured fields that can be queried at runtime. This approach simplifies adding new models, detecting feature support, and adapting to model updates without requiring extensive code changes.

For example, instead of:
```rust
fn supports_vision(&self) -> bool {
    match self {
        Self::Gpt4o | Self::Gpt4_1 | Self::Claude3_5Sonnet => true,
        _ => false,
    }
}
```

Use:
```rust
struct Model {
    id: String,
    name: String,
    capabilities: ModelCapabilities,
    // ...
}

struct ModelCapabilities {
    // ...
    supports: ModelSupportedFeatures,
}

struct ModelSupportedFeatures {
    #[serde(default)]
    vision: bool,
    // ...
}

impl Model {
    pub fn supports_vision(&self) -> bool {
        self.capabilities.supports.vision
    }
}
```

This data-driven approach is more maintainable when integrating new AI models and reduces the risk of errors when model capabilities change. It also enables more efficient filtering and selection of models based on required capabilities.