---
title: Config precedence and canonical sources
description: 'Establish a single, explicit source-of-truth approach for configuration
  resolution: (1) honor user-supplied overrides first, (2) otherwise derive from the
  active context/environment, and (3) only then fall back to defaults; additionally,
  treat repository-level configuration/lock files as canonical entrypoints for developer
  tooling.'
repository: diegosouzapw/OmniRoute
label: Configurations
language: Other
comments_count: 2
repository_stars: 33162
---

Establish a single, explicit source-of-truth approach for configuration resolution: (1) honor user-supplied overrides first, (2) otherwise derive from the active context/environment, and (3) only then fall back to defaults; additionally, treat repository-level configuration/lock files as canonical entrypoints for developer tooling.

How to apply:
- CLI/config resolution: implement a consistent precedence order and pass required context through the full call chain.
- Never ignore an available active context (or env) just because a command has a “convenient” default (e.g., localhost).
- Dev tooling: don’t duplicate or move canonical root config/lock files (e.g., flake.nix/devbox.json/associated locks); changes require coordinating the tooling that consumes them.

Example (pattern for precedence):
```js
export async function runLogsCommand(opts = {}) {
  const baseUrl =
    opts.baseUrl ||
    opts["base-url"] ||
    getBaseUrl({ context: opts.context }); // derived from active context/env

  // ...use baseUrl to build requests
}
```
