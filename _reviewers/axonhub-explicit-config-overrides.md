---
title: Explicit Config Overrides
description: 'Implement configuration in a way that is predictable: define defaults
  centrally, keep early rollout scope narrow (prefer deployment-level defaults), and
  make override semantics explicit.'
repository: looplj/axonhub
label: Configurations
language: Go
comments_count: 3
repository_stars: 4808
---

Implement configuration in a way that is predictable: define defaults centrally, keep early rollout scope narrow (prefer deployment-level defaults), and make override semantics explicit.

Apply this standard:
1) Set defaults in the conf package (single source of truth). Avoid scattering “fallback” values across business logic.
2) Use deployment-level defaults first for new config knobs; defer per-channel/UI/schema expansion until there’s product/runtime backing.
3) For any “override” configuration, choose and document semantics clearly.
   - If the override is meant to fully take over for the period, treat it as full replacement: only the explicitly configured item codes apply; all others become 0 (or equivalent “unset” behavior), rather than silently merging.

Example (full-replacement override pattern + deploy-level default):

```go
// conf package should provide defaults, not business logic.
// e.g., conf.DefaultXXX

func codexImageMainModel() string {
    // deployment-level default (via env) only; keep scope limited initially
    if v := strings.TrimSpace(os.Getenv("AXONHUB_CODEX_IMAGE_MAIN_MODEL")); v != "" {
        return v
    }
    return defaultImageMainModel
}

func effectiveItems(now time.Time, schedule *Schedule, base Items) Items {
    if schedule == nil {
        return base
    }
    if override := findMatchingOverride(now, schedule); override != nil {
        // full replacement: override.Items is the complete effective set
        return override.Items
    }
    return base
}
```

Outcome: fewer surprises during runtime, easier debugging, and safer incremental rollout of configuration-driven features.