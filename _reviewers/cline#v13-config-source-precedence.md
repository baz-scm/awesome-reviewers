---
title: Config source precedence
description: Define and enforce a single, shared source-of-truth for derived configuration,
  with explicit precedence across env/config/provider settings—then reuse it everywhere
  (CLI, desktop/webview, runtime, UI).
repository: cline/cline#v13
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 70874
---

Define and enforce a single, shared source-of-truth for derived configuration, with explicit precedence across env/config/provider settings—then reuse it everywhere (CLI, desktop/webview, runtime, UI).

Applies when:
- A value can come from env vars, provider settings (e.g., `baseUrl`), or runtime defaults.
- UI needs to show the same “effective” behavior the runtime will use.
- Eligibility/enablement logic has to match across components.

Standards:
1) Centralize derived mappings in shared helpers
- If you need “backend → correct environment/app URL” (or similar), compute it once via a shared function and pass the resolved value down.

Example pattern:
```ts
// Shared helper (idea)
function resolveAppBaseUrl(apiBaseUrl: string): string | undefined {
  // maps trailing-slash-insensitive backend baseUrl -> correct app base url env
}

// CLI/desktop: resolve once from the backend they will actually call
const apiBaseUrl = resolveAccountApiBaseUrl(/* provider/env resolution */);
const appBaseUrl = apiBaseUrl ? resolveAppBaseUrl(apiBaseUrl) : undefined;

// UI/webview uses the resolved appBaseUrl (no re-resolution per refresh)
const privacyUrl = appBaseUrl ? `${appBaseUrl}/privacy` : undefined;
```

2) Codify precedence and test it
- Always document and test ordering like: CLI flag > auth subcommand flag > env fallback > default.
- For config overrides: “caller-supplied wins; derived defaults only apply when unset.”

3) Reuse core logic for eligibility/parsing
- Don’t maintain independent copies of “is provider usable / should onboarding be skipped” or “frontmatter enablement parsing.”
- Import and use the same core function(s) so behavior cannot drift.

4) Resolve stable config once when possible
- If the app won’t switch backends/environments after startup, compute derived values at startup and reuse them (avoid per-refresh recomputation that can reintroduce source mismatches).

5) Add regression tests for drift-prone cases
- Include cases with missing keys/URL, staging vs prod overrides, and negatable CLI flags that could silently clobber env fallback.

Outcome: consistent behavior across CLI, desktop, and runtime, fewer “wrong environment”/“wrong effective config” bugs, and easier maintenance because precedence and parsing rules live in one place.