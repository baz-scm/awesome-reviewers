---
title: Explicit config resolution
description: Configuration values (env vars, URLs, feature flags, paths) must be resolved
  through one canonical, explicit path rather than relying on implicit inheritance
  or ad-hoc lookups scattered across the codebase.
repository: cline/cline;
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 70964
---

Configuration values (env vars, URLs, feature flags, paths) must be resolved through one canonical, explicit path rather than relying on implicit inheritance or ad-hoc lookups scattered across the codebase.

- Never assume a subprocess, worker, or sandbox inherits the host's environment or config variables. Explicitly copy every setting it needs (e.g. `CLINE_DIR`, `OLLAMA_HOST`) onto that process's env before spawning it, and add a regression test that proves a hostile/stale value in the parent env cannot leak through.
- When a value can come from multiple sources (CLI flag, env var, stored setting, provider config), define and document one precedence order, and resolve it by checking the actual source (e.g. `getOptionValueSource(...) === "cli"`), not just the possibly-defaulted value. Verify every combination (flag only, env only, both, neither) with a test matrix.
- Environment-specific values (base URLs, endpoints) must be derived from a single shared resolver that maps the *actually resolved* backend/config to its environment, instead of two independent lookups that can disagree (e.g. a provider's resolved `baseUrl` vs. a separately-read `appBaseUrl`). When the resolver can't match a known environment, fail safe (hide the link/feature) rather than defaulting to production.
- Keep one canonical field/store per setting (e.g. one `apiKey` on `ProviderSettings`); don't reintroduce parallel legacy fields that can drift out of sync.
- Build/test tooling that touches config must run against an isolated, temp config directory (set `HOME`, `CLINE_DIR`, `CLINE_HUB_DISCOVERY_PATH`, etc. explicitly) so it never reads or mutates a developer's real configuration.

Example of explicit precedence resolution:
```ts
const authMouse =
	(authCmd.getOptionValueSource("mouse") === "cli" ? authCmd.opts().mouse : undefined) ??
	(program.getOptionValueSource("mouse") === "cli" ? program.opts().mouse : undefined);
// fallback to env only happens downstream, and only when neither flag was explicitly set
```