---
title: Unify Config Resolution
description: Ensure every feature derives configuration from a single authoritative
  resolution path, and apply the same rules consistently across runtime logic, UI/link
  generation, and capability decisions.
repository: cline/cline#v2
label: Configurations
language: TypeScript
comments_count: 9
repository_stars: 70861
---

Ensure every feature derives configuration from a single authoritative resolution path, and apply the same rules consistently across runtime logic, UI/link generation, and capability decisions.

**Standards**
1. **Centralize resolution helpers**: If multiple parts need the same decision (e.g., provider usability, frontmatter enablement, base URL mapping, “is API key in env?”), expose/consume the shared helper from the core library instead of re-implementing it.
2. **Use the resolved target everywhere**: Once you resolve the “thing you actually hit” (provider backend baseUrl / selected remote / resolved provider id), downstream actions (privacy links, webview actions, push targets) must be derived from that exact resolved value—not from a different environment field.
3. **Resolve at the right lifecycle boundary**: If you don’t support changing backend/provider/environment after startup, resolve once at startup and pass the resolved value through; don’t re-resolve on every account refresh.
4. **Feature flags must not break existing capability**: When disabled, report accurately without breaking pre-existing state by applying the same per-run restore/availability rule used by the underlying system.
5. **Tests must be environment-isolated**: When configuration depends on environment/discovery paths, run smoke/tests in a temp home/data directory and override discovery variables so tests don’t touch or rely on a developer’s real environment.

**Example pattern (base URL mapping + lifecycle)**
```ts
// startup (sidecar/index or app bootstrap)
const backendBaseUrl = await resolveAccountBackendBaseUrlOnce(/* provider/account context */);
const appBaseUrl = resolveClineAppBaseUrl(backendBaseUrl); // shared helper
ctx.clineAppBaseUrl = appBaseUrl; // may be undefined

// command handler (no re-resolution per refresh)
export async function get_cline_app_base_url() {
  return { appBaseUrl: ctx.clineAppBaseUrl }; // UI can hide when undefined
}
```

Adopting this prevents mismatches like “UI points to a different environment than the backend,” “provider works via env but UI refuses,” or “duplicated enable/disable parsing drift” across modules.