---
title: Centralize config resolution
description: 'When code depends on environment/provider configuration, treat configuration
  resolution as a single, canonical step and reuse it everywhere.


  **Standard**'
repository: cline/cline#v9
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 70868
---

When code depends on environment/provider configuration, treat configuration resolution as a single, canonical step and reuse it everywhere.

**Standard**
1. **Resolve once** (startup or once per operation) for values that must stay consistent (e.g., app base URL, selected URLs/targets, provider-derived defaults). Avoid re-resolving on every refresh/account update.
2. **Use shared helpers** for canonical mappings (e.g., backend base URL → environment-specific app URL; provider env vars → “is this a real API key?”). Don’t duplicate selection logic in multiple places.
3. **Make precedence explicit** for fallback chains: **caller-supplied override > provider manifest/runtime rules > environment/global defaults**. Never silently mix different sources.
4. **Avoid hardcoded placeholders/tags** (like `latest`)—prefer exported version constants and exact values.
5. **Add regression tests** that assert the resolved value is the one used to construct all dependent links/behaviors.

**Example pattern**
```ts
// Resolve canonical values once
const appBaseUrl = resolveClineAppBaseUrl(apiBaseUrl); // shared helper

// Build all dependent URLs from the canonical value
const privacyUrl = appBaseUrl
  ? `${appBaseUrl}/privacy/cli`
  : undefined; // hide instead of linking to a different environment

// Precedence: caller override > provider defaults > env
const modelId = callerModelId
  ?? providerManifest.defaultModelId
  ?? process.env.CLINE_DEFAULT_MODEL_ID;
```

Applying this prevents drift such as “link points to a different environment than the backend actually hit,” inconsistent remote/target selection, or UI/onboarding logic diverging from runtime behavior.