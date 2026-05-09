---
title: Robust config handling
description: 'Treat configuration as a stable, privacy-safe contract: it must load
  without breaking the whole file, resolve safely at apply-time, use platform-correct
  paths, and (for significant changes) be shipped behind feature flags with explicitly
  defined non-lossy toggle behavior.'
repository: warpdotdev/warp
label: Configurations
language: Markdown
comments_count: 5
repository_stars: 56893
---

Treat configuration as a stable, privacy-safe contract: it must load without breaking the whole file, resolve safely at apply-time, use platform-correct paths, and (for significant changes) be shipped behind feature flags with explicitly defined non-lossy toggle behavior.

Apply these rules when you change or add configuration, settings, or config-driven behavior:

1) Prefer Settings persistence over ephemeral UI
- If a user option must apply across multiple surfaces (panels, embedded views, etc.), store it in Settings (or a persisted setting), not only as a toolbar-only toggle.

2) Feature-flag major behavior changes
- Gate substantial features behind a named flag.
- Define defaults per channel (e.g., stable off, dev/preview on).
- Ensure flag-off behavior is non-lossy: persisted state remains on disk, and rendering/apply-time application changes are well-defined.
- Add integration tests that verify round-trip behavior when flipping the flag.

3) Make config parsing fail-soft; validate at apply-time
- Do not make “unknown theme/name/value” fail entire YAML/TOML loads.
- Use types like `Option<String>` for free-form references at the schema layer, then resolve into canonical internal types during application.
- When a value is unknown, log a warning once per load/apply and fall through to the next resolution layer for that entry only.

4) Resolve paths centrally and pass resolved values
- Never require downstream components/agents to guess locations like `~/.warp*/`.
- Use the project’s path helpers to compute the correct config directory/file path for the current OS (and ensure it’s reachable in test builds).
- Prefer embedding the resolved path in templated contexts over instructions to infer it.

5) Treat sensitive config data as local-only; redact diagnostics
- If configuration keys/values can encode sensitive user/project/org context, set sync off (local/private) and avoid including raw paths/keys in logs.
- Use stable redacted identifiers (hashes) for warnings so users can correlate repeated messages without leaking raw data.

6) Keep bundled/agent-exposed skills aligned with the schema
- If your config schema adds an option (e.g., `working_directory`), update the bundled skill so it explains defaults and supports the override parameter with correct example structure.

Example pattern (fail-soft + apply-time resolution + safe warning):
```rust
// Schema layer: never fails load on unknown values
#[derive(Deserialize)]
struct Entry { theme_ref: Option<String> }

// Apply-time resolution (per-entry fallback)
fn apply_entry(entry: Entry) {
    if let Some(raw) = entry.theme_ref {
        match resolve_theme_ref(&raw) {
            Some(theme) => set_effective_theme(theme),
            None => {
                let id = redacted_key_id(&raw); // or for the config key
                log::warn!("config[hash={}] unknown theme '{}'; skipping entry", id, raw);
                // fall through to next resolution layer
            }
        }
    }
}
```

Use this standard as a checklist during reviews for anything under the “Configurations” umbrella: settings schema changes, feature-flag rollout wiring, config-driven rendering/application, path handling, and privacy/sync behavior.