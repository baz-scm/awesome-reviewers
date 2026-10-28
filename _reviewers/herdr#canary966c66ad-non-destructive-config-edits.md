---
title: Non-destructive config edits
description: 'When programmatically reading or rewriting a user''s config file (TOML,
  YAML, JSON, etc.), treat the existing content as precious: parse it with a real
  parser instead of ad-hoc line splicing, preserve comments, quoting, inline formatting,
  and section ordering that the edit doesn''t touch, and only mutate the specific
  key/value being changed. Validate the...'
repository: ogulcancelik/herdr#canary966c66ad
label: Configurations
language: Rust
comments_count: 7
repository_stars: 46332
---

When programmatically reading or rewriting a user's config file (TOML, YAML, JSON, etc.), treat the existing content as precious: parse it with a real parser instead of ad-hoc line splicing, preserve comments, quoting, inline formatting, and section ordering that the edit doesn't touch, and only mutate the specific key/value being changed. Validate the entire proposed result (including recovering from malformed input such as displaced BOMs) before any bytes are written, and write the file atomically so a failed or partial edit never corrupts the original or leaves orphaned side files (e.g. don't write an installed hook file before the settings file that references it has been successfully parsed and rewritten). When surfacing config diagnostics to the user, make sure one category of problem (e.g. "unknown key") can't mask or override a more serious unrelated failure (e.g. an invalid section) — only use a specific, narrower message when it accounts for *all* reported diagnostics.

Example pattern to follow:
```rust
// Parse with a real parser, not string/line splicing.
let mut doc: DocumentMut = content.parse().map_err(|e| e.to_string())?;

// Mutate only the targeted value, leaving comments/formatting intact.
upsert_section_value(&mut doc, "update", "channel", "\"preview\"")?;

// Validate the full result before persisting.
let new_content = doc.to_string();
validate(&new_content)?;

// Write atomically; never leave the file half-written or out of sync
// with dependent artifacts.
atomic_write(path, new_content)?;
```
Add regression tests covering comments, quoting, inline/dotted tables, and malformed-input recovery to ensure edits remain byte-for-byte faithful outside the targeted change.