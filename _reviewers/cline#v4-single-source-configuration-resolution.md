---
title: Single-source configuration resolution
description: When deriving effective configuration values (URLs, feature availability,
  provider readiness, onboarding skips), resolve them from the same inputs using shared
  resolvers/helpers, then propagate the resolved result—don’t recompute it in separate
  layers.
repository: cline/cline#v4
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 70864
---

When deriving effective configuration values (URLs, feature availability, provider readiness, onboarding skips), resolve them from the same inputs using shared resolvers/helpers, then propagate the resolved result—don’t recompute it in separate layers.

Apply this standard:
- **Use one resolver per derived value**: e.g., if runtime resolves a backend base URL, derive any UI/link base URL from that exact resolved backend value using a shared helper.
- **Resolve once when runtime can’t change after startup**: if environment/provider/backend won’t switch during the session, compute at startup and pass the resolved value to UI/webviews instead of re-reading provider settings on refresh.
- **Avoid duplicated readiness/flags**: if the shared provider contract already provides metadata (e.g., API-key optional / configured readiness), don’t maintain a second unsynchronized session flag.
- **Unify feature flag semantics**: UI availability checks must use the same per-run resolution rules as the runtime (e.g., don’t read the raw setting independently when runtime uses a derived rule).
- **Define and implement precedence (CLI vs env vs config)**: for negatable CLI flags, don’t rely on raw option defaults; use the option’s value/source to decide whether to use the CLI value or fall back to env.

Example pattern for CLI/env precedence (negatable flags):
```ts
const cliValueProvided = authCmd.getOptionValueSource("mouse") === "cli";
const mouse = (cliValueProvided ? authCmd.opts().mouse : undefined)
  ?? (program.getOptionValueSource("mouse") === "cli" ? program.opts().mouse : undefined)
  ?? undefined; // then in runtime:
const useMouse = mouse ?? (process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0");
```

Rule of thumb: if two parts of the system show or act on “the same config-derived concept”, they must come from the same resolved value (not two separate computations with slightly different inputs).