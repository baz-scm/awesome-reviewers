---
title: Resolve config once, precedence-aware
description: Environment-derived configuration (base URLs, host names, backend overrides,
  startup timeouts, feature toggles) should be resolved exactly once, at process/session
  startup, and then cached or passed down through context rather than being re-derived
  on every call or request. For example, an app base URL or host name that depends
  on provider/environment...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 70984
---

Environment-derived configuration (base URLs, host names, backend overrides, startup timeouts, feature toggles) should be resolved exactly once, at process/session startup, and then cached or passed down through context rather than being re-derived on every call or request. For example, an app base URL or host name that depends on provider/environment settings belongs in a startup resolution step (e.g. `resolveSidecarClineAppBaseUrl()` writing to `ctx.clineAppBaseUrl`, or reading `HostRegistryInfo` populated once at boot) instead of being recomputed inside a hot path like `getStateToPostToWebview` or on every `get_cline_app_base_url` call — the app doesn't support switching backend/environment after startup, so there is no need to re-read provider settings each time.

When a config value can come from multiple sources (CLI flag, environment variable, stored setting, default), define and document an explicit precedence order and implement it carefully, since library defaults can silently break the chain. For instance, when resolving a `--no-mouse` flag that should fall back to `CLINE_NO_MOUSE`/`CLINE_MOUSE` env vars, don't read the negatable option's value directly — Commander defaults `--no-mouse` to `true`, which would clobber the env fallback. Instead, check whether the value was actually supplied (`getOptionValueSource("mouse") === "cli"`) before applying it, and feed the same resolved value through every call site rather than rebuilding it along the way.

Likewise, environment-specific runtime configuration (e.g. a custom local-server port) should be propagated consistently to subprocesses via the expected environment variables (e.g. setting `OLLAMA_HOST` from the saved base URL before spawning), and shared default values (timeouts, limits) that apply across multiple environments/clients should be set once based on real data rather than duplicated or diverged per platform without a documented reason.