---
title: Centralize config resolution
description: Resolve configuration values in one well-defined place and reuse that
  result everywhere, instead of letting each call site re-derive its own answer from
  raw settings. When a value can only change at startup (active account/backend, app
  base URL), compute it once during initialization and pass the resolved value down
  rather than re-reading provider settings...
repository: cline/cline#&&sleep 4
label: Configurations
language: TypeScript
comments_count: 8
repository_stars: 70980
---

Resolve configuration values in one well-defined place and reuse that result everywhere, instead of letting each call site re-derive its own answer from raw settings. When a value can only change at startup (active account/backend, app base URL), compute it once during initialization and pass the resolved value down rather than re-reading provider settings on every request or event. When combining an explicit, caller-supplied override with a derived default, write it as `override ?? derivedDefault` so the explicit value always wins — never let the derived branch silently take precedence. Centralize provider-specific knowledge (env var names, exclusion lists, default model IDs) in the shared config/llms package instead of duplicating it per consumer, so every call site applies identical rules for things like "is this provider configured." Configuration that must cross a process boundary — a spawned subprocess, a sandboxed worker, or a plugin — has to be explicitly copied onto that process's environment (e.g., `CLINE_DIR`, `OLLAMA_HOST`); child processes do not automatically inherit host-side module state. Finally, any tool that touches real configuration directories, such as build smoke tests or CI scripts, must isolate itself with its own env vars (`CLINE_DIR`, `CLINE_DATA_DIR`, `CLINE_HUB_DISCOVERY_PATH`) so it can never read or corrupt a developer's actual configuration.