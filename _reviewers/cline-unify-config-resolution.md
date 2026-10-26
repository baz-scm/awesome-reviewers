---
title: Unify config resolution
description: When the same setting (a base URL, a git remote, a host name, an API-key
  check, a bind-fallback flag) is resolved in more than one place, each implementation
  tends to drift and the app ends up showing or using inconsistent values (e.g. the
  webview linking to production while the account service actually hit staging, or
  the manifest showing a different repo...
repository: cline/cline
label: Configurations
language: TypeScript
comments_count: 8
repository_stars: 70886
---

When the same setting (a base URL, a git remote, a host name, an API-key check, a bind-fallback flag) is resolved in more than one place, each implementation tends to drift and the app ends up showing or using inconsistent values (e.g. the webview linking to production while the account service actually hit staging, or the manifest showing a different repo than the one being pushed to). Put the resolution logic in one shared function/module and have every caller (CLI, sidecar, webview, TUI) use it, instead of re-implementing the same lookup with slightly different rules.

Define precedence explicitly and test it, especially when combining CLI flags, env vars, caller-supplied options, and library-derived defaults. Caller-supplied/explicit values must win over derived defaults, and a derived default must only fill in when nothing more specific was provided (e.g. `allowBindFallback: callerValue ?? !hasExplicitEndpoint`, not the reverse). Watch out for libraries (e.g. Commander's negatable flags) that silently populate a value to `true`/`false` even when the user didn't pass it — check `getOptionValueSource` or an equivalent "was this actually set" signal rather than trusting the raw value, so a lower-priority source (env var) isn't clobbered.

For settings that cannot change during the lifetime of a process (active environment, backend, host name, app base URL), resolve them once at startup and store/pass the resolved value down, rather than re-deriving them from provider settings or doing a cross-process lookup on every call. This avoids unnecessary repeated work and guarantees every part of the app agrees on the same value for the whole session.

Example pattern to follow:
```ts
// resolved once, from one place, at startup
ctx.clineAppBaseUrl = resolveSidecarClineAppBaseUrl(providerSettings, envConfig)

// every consumer just reads the resolved value
function handleGetClineAppBaseUrl() {
  return ctx.clineAppBaseUrl
}
```
and for precedence:
```ts
const mouse =
  input.mouse !== undefined
    ? input.mouse
    : process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0"
```