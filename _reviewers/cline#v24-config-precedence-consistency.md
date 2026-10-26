---
title: Config precedence consistency
description: When code makes environment- or config-dependent decisions, enforce a
  single, consistent resolution path and precedence order across the call chain—no
  duplicated rules.
repository: cline/cline#v24
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 70891
---

When code makes environment- or config-dependent decisions, enforce a single, consistent resolution path and precedence order across the call chain—no duplicated rules.

**Standards**
1. **Resolve once, reuse everywhere**: compute the resolved config value (e.g., backend/app base URL, derived endpoints, or repo target) in one place (prefer a shared helper), then build all dependent behavior (links, requests, telemetry) from that same resolved value.
2. **Declare and implement precedence explicitly**:
   - **explicit caller/option** (when provided) **wins**
   - else **explicit CLI flag** (only if the user supplied it) wins
   - else **environment variables**
   - else **derived defaults**
3. **Negatable/boolean CLI flags must not clobber env**: don’t read the raw option value when a library applies defaults; detect whether the option was explicitly provided.
4. **Feature flags must be behavior-scoped**: if a flag disables future actions, do not retroactively invalidate existing computed state; use the same underlying per-run rule used by the “restore”/consumer path.
5. **Unify matching logic across components**: if runtime and UI/onboarding both decide “what counts as a valid setting,” they must share the same exclusion/precedence rules.

**Example: explicit CLI-vs-env precedence for negatable flags**
```ts
import type { Command } from "commander";

function resolveUseMouse(cmd: Command, env: NodeJS.ProcessEnv) {
  // Commander sets a negatable flag default; only treat it as CLI-provided
  // when it was actually specified by the user.
  const cliSupplied = cmd.getOptionValueSource("mouse") === "cli";
  const cliValue = cliSupplied ? (cmd.opts() as { mouse?: boolean }).mouse : undefined;

  return cliValue ?? (env.CLINE_NO_MOUSE !== "1" && env.CLINE_MOUSE !== "0");
}
```

**Example: derive URLs from the resolved backend once**
```ts
// Pseudocode: resolve backend once, then map to the correct environment-aware app base.
const apiBaseUrl = await resolveAccountApiBaseUrl(/* ... */);
const appBaseUrl = resolveClineAppBaseUrl(apiBaseUrl); // shared helper
const privacySettingsUrl = appBaseUrl ? `${appBaseUrl}/privacy` : undefined;
```