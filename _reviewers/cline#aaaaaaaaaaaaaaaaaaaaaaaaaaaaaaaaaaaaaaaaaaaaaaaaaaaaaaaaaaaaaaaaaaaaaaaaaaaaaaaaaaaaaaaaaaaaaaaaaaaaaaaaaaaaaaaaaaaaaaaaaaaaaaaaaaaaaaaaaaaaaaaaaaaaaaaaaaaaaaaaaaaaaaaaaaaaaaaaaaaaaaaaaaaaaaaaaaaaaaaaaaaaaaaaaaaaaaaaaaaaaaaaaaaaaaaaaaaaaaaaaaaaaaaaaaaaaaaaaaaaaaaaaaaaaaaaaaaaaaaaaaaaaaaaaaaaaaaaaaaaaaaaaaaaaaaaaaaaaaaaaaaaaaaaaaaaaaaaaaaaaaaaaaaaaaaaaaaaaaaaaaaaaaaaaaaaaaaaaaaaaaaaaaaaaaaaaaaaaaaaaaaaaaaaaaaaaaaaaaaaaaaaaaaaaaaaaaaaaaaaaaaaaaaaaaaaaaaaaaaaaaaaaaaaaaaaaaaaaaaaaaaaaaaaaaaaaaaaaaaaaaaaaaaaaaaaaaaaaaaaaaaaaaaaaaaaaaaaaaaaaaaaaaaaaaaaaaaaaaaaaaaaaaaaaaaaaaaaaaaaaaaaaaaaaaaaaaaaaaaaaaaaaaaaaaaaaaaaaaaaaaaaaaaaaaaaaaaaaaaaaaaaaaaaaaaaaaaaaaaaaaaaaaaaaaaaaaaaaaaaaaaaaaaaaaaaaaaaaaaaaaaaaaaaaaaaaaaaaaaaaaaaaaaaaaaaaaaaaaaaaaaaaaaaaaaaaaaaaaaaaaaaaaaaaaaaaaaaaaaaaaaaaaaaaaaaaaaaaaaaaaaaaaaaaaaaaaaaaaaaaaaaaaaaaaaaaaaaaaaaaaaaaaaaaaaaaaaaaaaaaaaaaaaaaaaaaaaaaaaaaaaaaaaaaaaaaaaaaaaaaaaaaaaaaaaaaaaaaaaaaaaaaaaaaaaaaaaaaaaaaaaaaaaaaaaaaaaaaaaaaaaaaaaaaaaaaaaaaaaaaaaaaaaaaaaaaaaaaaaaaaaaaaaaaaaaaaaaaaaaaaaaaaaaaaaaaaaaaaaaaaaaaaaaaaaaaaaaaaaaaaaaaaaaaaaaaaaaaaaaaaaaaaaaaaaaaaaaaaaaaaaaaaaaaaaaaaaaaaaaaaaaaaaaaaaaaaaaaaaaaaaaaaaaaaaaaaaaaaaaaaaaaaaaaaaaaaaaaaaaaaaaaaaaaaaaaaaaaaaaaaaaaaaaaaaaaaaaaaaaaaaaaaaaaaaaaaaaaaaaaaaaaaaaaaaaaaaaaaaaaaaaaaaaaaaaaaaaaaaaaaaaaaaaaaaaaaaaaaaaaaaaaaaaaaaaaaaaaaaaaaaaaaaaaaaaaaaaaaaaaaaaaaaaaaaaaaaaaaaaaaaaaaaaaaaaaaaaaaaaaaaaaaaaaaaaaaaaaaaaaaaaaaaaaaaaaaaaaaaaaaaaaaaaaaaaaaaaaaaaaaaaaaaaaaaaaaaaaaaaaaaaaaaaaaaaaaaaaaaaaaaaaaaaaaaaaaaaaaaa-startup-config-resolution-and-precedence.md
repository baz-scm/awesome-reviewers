---
title: Startup config resolution and precedence
description: Resolve environment-derived configuration (app base URLs, host names,
  provider overrides, timeouts) once during startup/initialization and cache the result,
  rather than re-deriving it on every call. If the app's lifecycle doesn't allow switching
  environments or accounts after launch, there's no need to re-read provider settings
  or re-query the host bridge...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 70965
---

Resolve environment-derived configuration (app base URLs, host names, provider overrides, timeouts) once during startup/initialization and cache the result, rather than re-deriving it on every call. If the app's lifecycle doesn't allow switching environments or accounts after launch, there's no need to re-read provider settings or re-query the host bridge each time a value is requested — read it once into context (e.g. `ctx.clineAppBaseUrl`, `HostRegistryInfo`) and have downstream code consume the cached value.

When a setting can come from multiple sources (CLI flag, environment variable, explicit caller-supplied option, or a value computed from other config), define and test an explicit precedence order, and make sure it's actually wired into the real runtime entry point rather than a test-only code path:
- An explicitly caller-supplied option must always win over an internally computed default (e.g. `allowBindFallback` from a caller should override the value derived from `hasExplicitEndpoint`: `options.allowBindFallback ?? !hasExplicitEndpoint`).
- A more specific scope wins over a less specific one, which wins over an environment-variable fallback — e.g. a subcommand flag beats the root flag, which beats `CLINE_NO_MOUSE`/`CLINE_MOUSE`. Use the option's value-source (e.g. Commander's `getOptionValueSource`) rather than the raw flag value when the flag negates and defaults to a truthy value, so an unset flag doesn't silently clobber the env fallback.
- Add tests covering every combination of sources (flag only, env only, both, neither) to lock in the resolved precedence.

When picking default values for tunable settings (timeouts, retry counts, feature toggles), base them on measured data (e.g. telemetry of real failure/success distributions) rather than guesses, and document the reasoning and trade-offs next to the constant so future changes understand the constraints that produced it.