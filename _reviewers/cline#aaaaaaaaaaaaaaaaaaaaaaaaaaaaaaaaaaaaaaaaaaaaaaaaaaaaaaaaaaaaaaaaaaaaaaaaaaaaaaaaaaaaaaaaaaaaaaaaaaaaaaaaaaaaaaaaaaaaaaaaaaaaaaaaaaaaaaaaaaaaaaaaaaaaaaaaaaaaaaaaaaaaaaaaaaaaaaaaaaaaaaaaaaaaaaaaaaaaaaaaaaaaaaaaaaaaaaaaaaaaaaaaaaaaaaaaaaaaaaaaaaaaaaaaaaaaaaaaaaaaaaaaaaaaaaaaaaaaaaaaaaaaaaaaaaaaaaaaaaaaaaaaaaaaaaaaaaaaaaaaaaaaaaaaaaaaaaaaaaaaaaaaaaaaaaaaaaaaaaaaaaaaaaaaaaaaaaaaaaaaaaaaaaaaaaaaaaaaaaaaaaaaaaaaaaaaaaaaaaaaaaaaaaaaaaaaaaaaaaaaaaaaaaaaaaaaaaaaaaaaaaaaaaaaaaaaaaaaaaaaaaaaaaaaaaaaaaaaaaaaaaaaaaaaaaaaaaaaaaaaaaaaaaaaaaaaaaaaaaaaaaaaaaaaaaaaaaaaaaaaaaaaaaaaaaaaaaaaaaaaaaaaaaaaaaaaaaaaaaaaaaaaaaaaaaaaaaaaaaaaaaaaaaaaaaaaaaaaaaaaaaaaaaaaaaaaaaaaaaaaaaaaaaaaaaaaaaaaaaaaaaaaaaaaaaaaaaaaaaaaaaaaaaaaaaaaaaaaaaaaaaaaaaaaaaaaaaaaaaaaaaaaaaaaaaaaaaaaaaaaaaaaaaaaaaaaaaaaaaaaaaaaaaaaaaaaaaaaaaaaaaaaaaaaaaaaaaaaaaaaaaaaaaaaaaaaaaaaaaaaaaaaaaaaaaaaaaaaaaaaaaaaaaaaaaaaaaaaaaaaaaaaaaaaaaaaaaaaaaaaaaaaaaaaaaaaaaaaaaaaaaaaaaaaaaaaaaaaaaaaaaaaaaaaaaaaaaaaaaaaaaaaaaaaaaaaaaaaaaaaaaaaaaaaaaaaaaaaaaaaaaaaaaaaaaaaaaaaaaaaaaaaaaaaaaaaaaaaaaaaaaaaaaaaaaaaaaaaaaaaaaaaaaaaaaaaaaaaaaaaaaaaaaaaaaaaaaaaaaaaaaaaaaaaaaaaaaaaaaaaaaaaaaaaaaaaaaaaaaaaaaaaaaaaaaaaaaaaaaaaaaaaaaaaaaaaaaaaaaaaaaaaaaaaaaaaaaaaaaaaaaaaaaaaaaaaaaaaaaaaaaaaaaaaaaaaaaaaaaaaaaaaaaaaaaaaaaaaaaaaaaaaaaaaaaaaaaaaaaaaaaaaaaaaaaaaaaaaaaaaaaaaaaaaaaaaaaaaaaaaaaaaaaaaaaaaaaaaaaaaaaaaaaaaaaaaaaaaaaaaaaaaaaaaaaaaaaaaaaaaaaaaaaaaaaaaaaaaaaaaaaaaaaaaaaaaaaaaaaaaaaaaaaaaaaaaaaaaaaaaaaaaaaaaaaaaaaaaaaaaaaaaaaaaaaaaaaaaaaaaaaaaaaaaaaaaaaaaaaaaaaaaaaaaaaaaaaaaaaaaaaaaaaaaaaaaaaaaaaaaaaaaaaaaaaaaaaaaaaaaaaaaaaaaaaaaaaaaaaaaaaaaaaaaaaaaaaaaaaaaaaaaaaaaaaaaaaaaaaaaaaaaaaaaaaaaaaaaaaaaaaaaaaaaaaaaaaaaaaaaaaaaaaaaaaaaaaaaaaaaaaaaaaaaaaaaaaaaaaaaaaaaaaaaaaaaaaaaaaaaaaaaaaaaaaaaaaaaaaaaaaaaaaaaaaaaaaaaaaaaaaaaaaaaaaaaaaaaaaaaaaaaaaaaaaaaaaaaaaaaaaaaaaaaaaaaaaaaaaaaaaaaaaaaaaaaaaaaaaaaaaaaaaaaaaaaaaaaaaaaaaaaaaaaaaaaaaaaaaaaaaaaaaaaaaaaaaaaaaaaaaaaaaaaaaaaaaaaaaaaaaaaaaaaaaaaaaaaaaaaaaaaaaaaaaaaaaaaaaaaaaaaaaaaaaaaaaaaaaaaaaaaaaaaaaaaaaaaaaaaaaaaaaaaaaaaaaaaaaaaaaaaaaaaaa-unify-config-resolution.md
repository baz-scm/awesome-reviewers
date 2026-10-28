---
title: Unify config resolution
description: When a configuration value (default model id, provider readiness, base
  URL, git remote, mouse/env toggle, directory path) can be derived in more than one
  place, keep its resolution in a single, canonical function with a clearly documented
  precedence order (e.g. explicit CLI flag > stored setting > environment variable
  > provider-manifest default > hardcoded...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Configurations
language: TypeScript
comments_count: 8
repository_stars: 70970
---

When a configuration value (default model id, provider readiness, base URL, git remote, mouse/env toggle, directory path) can be derived in more than one place, keep its resolution in a single, canonical function with a clearly documented precedence order (e.g. explicit CLI flag > stored setting > environment variable > provider-manifest default > hardcoded fallback), and make every caller use that same resolver instead of re-implementing or duplicating the rule. Several issues stemmed from divergence here: handoff git preparation and the workspace manifest picked the "primary remote" with two different rules; a `providerConfigured` flag duplicated readiness already computed by the provider catalog; and a connector's model fallback used a single hardcoded literal instead of the provider's own manifest default.

Resolve values that are fixed for the process lifetime (app base URL, startup timeouts, data directories) once at a stable boundary — e.g. at process/app startup — and pass the resolved value explicitly to downstream code and subprocesses, rather than re-reading settings or environment on every call. For values that cross into a sandbox, worker, or subprocess, copy them into that process's environment explicitly instead of relying on an in-process module variable that the child can't see.

Respect precedence correctly when mixing flags and environment variables — an explicit flag must never be silently overridden by an env fallback:

```ts
const mouse =
	(authCmd.getOptionValueSource("mouse") === "cli" ? authCmd.opts().mouse : undefined) ??
	(program.getOptionValueSource("mouse") === "cli" ? program.opts().mouse : undefined);
// env fallback only applies when neither flag was explicitly passed
const useMouse = mouse !== undefined ? mouse : env.CLINE_NO_MOUSE !== "1" && env.CLINE_MOUSE !== "0";
```

Finally, when build or test tooling spawns processes that would otherwise read or write real configuration (hub discovery files, provider settings, home directory), explicitly point every relevant env var (`CLINE_DIR`, `CLINE_HUB_DISCOVERY_PATH`, `HOME`, etc.) at an isolated temporary location so tooling runs never touch a developer's actual configuration.