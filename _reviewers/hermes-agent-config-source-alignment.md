---
title: Config source alignment
description: 'Behavioral configuration must be documented and wired through the supported
  config system, with examples matching the actual runtime resolution.


  Apply these rules:'
repository: nousresearch/hermes-agent
label: Configurations
language: Markdown
comments_count: 10
repository_stars: 221948
---

Behavioral configuration must be documented and wired through the supported config system, with examples matching the actual runtime resolution.

Apply these rules:
1) **Non-secret settings → `config.yaml`**
   - Don’t introduce or document new ad-hoc non-secret env mechanisms (e.g., `HERMES_*`) unless there is an explicit, accepted config-system feature.
   - Place user-facing behavioral settings under `~/.hermes/config.yaml`, namespaced by the owning feature/skill (e.g., `kairos:`, `tts:`, etc.).

2) **`.env` is secrets-only**
   - If a setting is not secret, document it in `~/.hermes/config.yaml`.
   - Keep credentials (API keys, tokens) in `.env` / secret stores.

3) **Docs must match real default resolution**
   - If a doc/example claims a default backend, ensure it is true for the actual resolution logic (e.g., extraction vs search-only).
   - When an option explicitly replaces defaults (e.g., providing a list), document the complete default set and the replacement behavior.

4) **Installation/runtime paths must be accurate**
   - When referencing scripts or artifacts, use the post-install location or provide a configurable `SKILL_DIR`/path instead of repo-relative paths.

5) **Avoid documenting unsupported keys until implemented**
   - If code/feature flags exist in docs but are not implemented in main yet, gate or defer the documentation.

Example (`~/.hermes/config.yaml`):
```yaml
# Non-secret behavior
kairos:
  enabled: true
  schedule: "weekly"

terminal:
  shell_init_files: []   # explicit list replaces OS defaults
```
Example (`.env`):
```bash
OPENAI_API_KEY=***
# secrets only
```