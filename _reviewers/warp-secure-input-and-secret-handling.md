---
title: Secure Input and Secret Handling
description: 'Adopt a consistent rule: anything coming from persistence, other platforms/accounts,
  terminal escape sequences, or secret-managed inputs must be validated/normalized
  and handled with collision-safe, non-injectable, non-leaky logic.'
repository: warpdotdev/warp
label: Security
language: Rust
comments_count: 8
repository_stars: 56893
---

Adopt a consistent rule: anything coming from persistence, other platforms/accounts, terminal escape sequences, or secret-managed inputs must be validated/normalized and handled with collision-safe, non-injectable, non-leaky logic.

Apply this as standards:
- **Path portability & sync safety:** When persisting selections that may be synced, only mark as “syncable” if you can reliably interpret it under the current installation root. For custom theme paths, serialize as relative *only* when the absolute path is under the current `themes_dir()`. Preserve “foreign” absolute paths (don’t attempt partial cross-platform legacy inference).
- **Test traversal + platform differences:** Include unit tests for `..`/parent traversal behavior and add Windows-specific coverage where paths/roots differ.
- **Shell command construction:** Never interpolate user- or data-derived strings into shell commands without a quoting strategy. Use a single helper (e.g., POSIX-safe single-quote escaping) and route all shell-sensitive formatting through it.
- **Secret injection precedence:** When turning secrets into environment/config, define precedence and do not override worker-injected env vars. Insert typed auth secrets atomically, and skip on collisions to avoid unintended behavior or privilege changes.
- **Secret file permissions:** When writing secret-bearing config files, create parent dirs if needed and enforce restrictive permissions (e.g., `0o600`) on Unix.
- **Parsing hardening & logging:** Avoid panics on malformed/unexpected structured input (use bounds checks/early exits). Don’t log raw untrusted substrings at debug/info levels if terminal/PTY content could contain echoed secrets.
- **Endpoint/target allowlists:** Prevent local-only configuration (e.g., local Ollama URLs) from being sent through remote/request settings.

Example patterns (condensed):
```rust
// 1) Shell quoting helper
fn shell_single_quote(value: &str) -> String {
    format!("'{}'", value.replace("'", "'\\''"))
}

// 2) Secret env insertion with collision safety
fn build_secret_env_vars(secrets: &HashMap<String, ManagedSecretValue>) -> HashMap<OsString, OsString> {
    let mut env_vars = HashMap::new();
    for (secret_key, secret) in secrets {
        // typed secrets: if any env var is already set non-empty, skip that secret entirely
        // (and never override existing process env)
        for (env_name, env_value) in typed_secret_entries(secret) {
            if std::env::var(env_name).is_ok_and(|v| !v.is_empty()) {
                continue; // collision: skip
            }
            env_vars.insert(OsString::from(env_name), OsString::from(env_value));
        }
    }
    env_vars
}
```
