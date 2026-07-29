---
title: Unified configuration semantics
description: 'Coding standard: Centralize configuration/credential semantics and never
  “re-derive” them in multiple places. Read from the real sources (env/config and
  provider-specific runtime credential caches), preserve provider identity during
  legacy interop, and let canonical normalizers own final resolution.'
repository: aaif-goose/goose
label: Configurations
language: Rust
comments_count: 6
repository_stars: 51876
---

Coding standard: Centralize configuration/credential semantics and never “re-derive” them in multiple places. Read from the real sources (env/config and provider-specific runtime credential caches), preserve provider identity during legacy interop, and let canonical normalizers own final resolution.

Apply this as follows:
- **Single source of truth**: Put “is this provider usable/configured?” logic in one shared function/module used by both server routes and the CLI picker.
- **Use real credential signals**: If credentials live outside declarative metadata (e.g., OAuth token caches), the usable gate must consult the provider’s inventory/registration signal rather than only `ProviderMetadata` config keys.
- **Correct precedence & explicitness**: Treat defaults differently from credentials. Don’t mark a provider usable just because a defaulted required key exists—require explicit setting and/or a real secret value.
- **Don’t short-circuit normalization**: Endpoints should avoid pre-filling fields that cause `normalize_*` logic to skip important normalization steps; pass raw model inputs to the canonical normalizer.
- **Legacy migration correctness**: When translating legacy flat keys to structured provider state, ensure updates apply to the **target provider** (not the currently active provider), and consider env overrides so persistence doesn’t accidentally attach to the wrong provider.

Example pattern (shared usable gate):
```rust
// Single source of truth used by both server + CLI
pub fn provider_is_usable(meta: &ProviderMetadata, provider_type: ProviderType) -> bool {
    // handle local override
    if meta.name == "local" { return true; }

    // OAuth/token-cache-backed providers must consult inventory/configured signals
    // (not just meta.config_keys)
    if meta.config_keys.iter().any(|k| k.oauth_flow) {
        return provider_inventory_configured(meta.name.as_str());
    }

    // For non-OAuth providers: require explicit config/secret presence (not only defaults)
    required_keys_all_present_and_secrets_real(meta)
}
```
