---
title: Single Config Truth
description: Ensure all code paths use the same configuration resolution logic (mapping
  + precedence) and, when supported, resolve it once and pass the resolved value downstream.
repository: cline/cline#v14
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 70876
---

Ensure all code paths use the same configuration resolution logic (mapping + precedence) and, when supported, resolve it once and pass the resolved value downstream.

Apply this by:
- **Use shared helpers** for config mapping/rules (e.g., backend/baseUrl→environment/appUrl, SDK frontmatter enable/disable semantics, provider env-key detection). Avoid duplicating “rules” in multiple packages.
- **Resolve once at startup** when your product doesn’t support switching backend/environment after startup. Cache the resolved values and pass them to UI/sidecars rather than re-resolving on account refresh.
- **Make precedence explicit** across CLI flags, env vars, and provider settings. For negatable flags (e.g., `--no-x`), rely on the option *value source* rather than the raw option value to avoid clobbering env fallbacks.
- **Avoid mismatched operational targets** caused by different selection rules (e.g., “what the UI shows” vs “what the command actually pushes”).

Example (explicit CLI/env precedence for a negatable flag + startup caching):
```ts
// 1) resolve once during startup/config build
const useMouse = (() => {
  if (authCmd.getOptionValueSource("mouse") === "cli") {
    return authCmd.opts().mouse; // may be true/false from --no-mouse
  }
  if (program.getOptionValueSource("mouse") === "cli") {
    return program.opts().mouse;
  }
  return process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0";
})();

ctx = {
  // cache resolved, mapped config values once
  resolvedAppBaseUrl: resolveClineAppBaseUrl(resolvedApiBaseUrl),
  useMouse,
};

// 2) downstream consumers use cached values (no re-resolution per refresh)
webview.postMessage({ type: "appBaseUrl", value: ctx.resolvedAppBaseUrl });
```

This prevents subtle production/staging mismatches, UI/actions divergence, and rule drift between UI, CLI, sidecar, and SDK layers.