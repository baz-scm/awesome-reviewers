---
title: AI model configuration consistency
description: Maintain consistent AI model metadata and configuration across all providers
  to prevent breaking changes and ensure reliable behavior. When adding new models
  or updating existing ones, always update corresponding token limits, default configurations,
  and provider mappings simultaneously.
repository: block/goose
label: AI
language: Rust
comments_count: 6
repository_stars: 19037
---

Maintain consistent AI model metadata and configuration across all providers to prevent breaking changes and ensure reliable behavior. When adding new models or updating existing ones, always update corresponding token limits, default configurations, and provider mappings simultaneously.

Key practices:
- Define model token limits centrally (e.g., in `models.rs`) rather than scattered across provider files
- Use constants for model defaults instead of hardcoded strings: `model.fast_model = Some(ANTHROPIC_DEFAULT_FAST_MODEL)`
- When updating model lists, preserve existing models that users depend on unless there's a compelling reason to remove them
- Ensure model metadata stays synchronized across providers - if a model is added to one provider's known models, verify its limits are defined in the central configuration

Example from the discussions:
```rust
// Good: Centralized model limits
static MODEL_SPECIFIC_LIMITS: Lazy<Vec<(&'static str, usize)>> = Lazy::new(|| {
    vec![
        ("gpt-4o", 128_000),
        ("claude-3-5-sonnet", 200_000),
        ("moonshotai/kimi-k2-instruct", 131_072), // Added with corresponding limit
    ]
});

// Good: Using constants for defaults
const ANTHROPIC_DEFAULT_FAST_MODEL: &str = "claude-3-5-haiku-latest";
model = model.with_fast(ANTHROPIC_DEFAULT_FAST_MODEL);
```

This prevents user disruption from inconsistent model behavior and ensures that model updates don't break existing workflows or introduce undefined behavior due to missing configuration.