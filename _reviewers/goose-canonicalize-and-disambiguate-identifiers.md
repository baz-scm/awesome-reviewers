---
title: Canonicalize and Disambiguate Identifiers
description: 'Ensure every place that *stores, looks up, validates, or returns* provider/model/function
  identifiers uses a clear internal naming contract:


  - **Canonicalize before lookup:** strip known version/date/suffix patterns from
  externally supplied model ids before querying registries (so variants like `-latest`,
  `-0709`, or Bedrock `-vN(:M)?` resolve to the same...'
repository: aaif-goose/goose
label: Naming Conventions
language: Rust
comments_count: 5
repository_stars: 51876
---

Ensure every place that *stores, looks up, validates, or returns* provider/model/function identifiers uses a clear internal naming contract:

- **Canonicalize before lookup:** strip known version/date/suffix patterns from externally supplied model ids before querying registries (so variants like `-latest`, `-0709`, or Bedrock `-vN(:M)?` resolve to the same canonical entry).
- **Disambiguate UI labels:** if a picker/selection returns only the displayed label, include enough internal identity (e.g., provider name) so multiple rows can’t map back ambiguously.
- **Scope validation to the correct boundary:** shared inbound validators must remain provider-agnostic; apply provider/API-specific limits only during outbound sanitization (and protect with regression tests).
- **Use semantic naming constants:** prefer `*_PROVIDER_NAME` (and other naming constants) over hard-coded provider strings.

Example (disambiguated picker label pattern):
```rust
// Build rows that always map back uniquely.
let mut entries: Vec<(String, String, String)> = vec![]; // (label, provider_name, model_id)
for (meta, _ptype) in &all {
    for m in models_for_meta {
        let mut label = format!("{}  ▸  {}", meta.display_name, m);
        // Ensure uniqueness even if display_name + model collide across providers.
        if collides_somehow { 
            label.push_str(&format!("  (provider:{})", meta.name));
        }
        entries.push((label, meta.name.clone(), m));
    }
}
```

Apply these rules anywhere you normalize model/provider identifiers or convert between internal ids and user-facing names, so naming stays consistent, lookups remain correct, and selections can’t mis-route.