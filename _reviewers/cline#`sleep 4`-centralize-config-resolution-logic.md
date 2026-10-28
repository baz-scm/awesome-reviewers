---
title: Centralize config resolution logic
description: Never let the same configuration value be derived independently in more
  than one place. When several code paths each compute an environment URL, a remote/repo
  target, a feature-enabled flag, or a "configured/ready" state from raw inputs, they
  will eventually disagree, and the bugs are often security- or correctness-critical
  (e.g. a staging override silently...
repository: cline/cline#`sleep 4`
label: Configurations
language: TypeScript
comments_count: 8
repository_stars: 70979
---

Never let the same configuration value be derived independently in more than one place. When several code paths each compute an environment URL, a remote/repo target, a feature-enabled flag, or a "configured/ready" state from raw inputs, they will eventually disagree, and the bugs are often security- or correctness-critical (e.g. a staging override silently opening a production link, a manifest pointing at a different repo than the one actually pushed to, the extension's frontmatter "enabled" check disagreeing with the SDK loader).

Apply this standard:
1. Pick one canonical resolver (a shared function/module or a single field on a shared config object) for each configuration concern, and make every consumer call or read it instead of reimplementing the logic. For example, instead of each host computing its own app base URL from environment variables, expose `resolveClineAppBaseUrl(apiBaseUrl)` from the shared package and have the CLI, sidecar, and webview all call it with the same resolved backend.
2. If the inputs to a resolver cannot change at runtime (e.g. startup environment, provider baseUrl override), resolve it once and store the result (e.g. on a context object) rather than recomputing it on every call or event.
3. When a value can come from multiple sources (CLI flag, environment variable, computed default, caller-supplied option), define and test an explicit precedence order, and make sure explicit/caller-supplied overrides always win over defaults:
```ts
const useMouse =
  input.mouse !== undefined
    ? input.mouse            // explicit flag/option wins
    : process.env.CLINE_NO_MOUSE !== "1" &&
      process.env.CLINE_MOUSE !== "0"; // env fallback only when unset
```
4. Verify the override is actually wired through every layer it passes (CLI parsing → command handler → runtime), not just into a parallel/test-only entry point — add a regression test that exercises the full chain for each supported combination.
5. Avoid duplicating a computed/derived config flag in a second data structure (e.g. a session-config boolean mirroring provider-catalog readiness); instead surface the single source of truth through the existing shared contract so there is nothing to keep in sync.

Following this avoids divergent behavior across hosts/environments and removes an entire class of "which implementation is correct" bugs.</description>
