---
title: Provider-agnostic API design
description: Design your API interfaces to be provider-agnostic rather than tightly
  coupled to specific service providers. This improves flexibility, maintainability,
  and makes future provider changes less disruptive.
repository: openai/codex
label: API
language: Rust
comments_count: 2
repository_stars: 31275
---

Design your API interfaces to be provider-agnostic rather than tightly coupled to specific service providers. This improves flexibility, maintainability, and makes future provider changes less disruptive.

Key practices:
1. Use generic naming conventions for constants, functions, and types
2. Centralize common API interaction code in core modules
3. Use configuration objects to inject provider-specific details
4. Create abstractions that can work with multiple providers

Example - Instead of:
```rust
const OPENAI_STREAM_IDLE_TIMEOUT_MS: u64 = 300_000;
const OPENAI_STREAM_MAX_RETRIES: u64 = 10;

// Direct provider-specific implementation
async fn generate_summary(transcript: &[TranscriptEntry], model: &str) -> Result<String> {
    // Provider-specific implementation
    let api_key = get_openai_api_key()?;
    let url = "https://api.openai.com/v1/chat/completions";
    // Rest of implementation...
}
```

Prefer:
```rust
const DEFAULT_STREAM_IDLE_TIMEOUT_MS: u64 = 300_000;
const DEFAULT_STREAM_MAX_RETRIES: u64 = 10;

// Provider-agnostic implementation using configuration
async fn generate_summary(
    transcript: &[TranscriptEntry],
    model: &str,
    config: &Config,
) -> Result<String> {
    // Use configuration for provider details
    let api_key = config.get_api_key()?;
    let base = config.model_provider.base_url.trim_end_matches('/');
    let url = format!("{}/chat/completions", base);
    // Rest of implementation...
}
```

This approach makes your codebase more resilient to changes in provider APIs and allows for easier testing and switching between different service providers.