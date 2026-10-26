---
title: Environment URL consistency
description: 'When environment/configuration drives external links or feature availability,
  treat it as a first-class, consistently-generated dependency.


  Apply these rules:'
repository: cline/cline#v30
label: Configurations
language: TSX
comments_count: 5
repository_stars: 70894
---

When environment/configuration drives external links or feature availability, treat it as a first-class, consistently-generated dependency.

Apply these rules:
1) Centralize env-aware URL generation
- Use one URL builder (based on resolved app base URL + attribution) for all account-related links in a view.
- Avoid mixing env-aware URLs with hardcoded production constants; ensure buttons/links follow the same environment.

2) Resolve stable configuration once
- Fetch configuration values that are environment-related (e.g., app base URL) once at startup (or once per app lifetime) and reuse them across account refreshes/reconnects.
- Keep account identity refresh separate from environment/config resolution.
- If initial lookup fails, rely on transport/subscription retry until it succeeds, then stop reloading on every refresh.

3) Keep derived account links local
- If a privacy/account link is only shown in a specific view, derive it in that view instead of publishing it through shared account context.
- Only put true shared config in context (e.g., environment base URL that does not depend on account refresh).

4) Keep UI placement aligned with the meaning of the setting
- Place “account privacy/data sharing” actions in the Account view, and “telemetry/error reporting” toggles under Telemetry; don’t duplicate links in the wrong settings section.

Example (pattern):
```ts
// Startup (once): resolve env config
const [appBaseUrl, setAppBaseUrl] = useState<string | undefined>();
useEffect(() => {
  void desktopClient.invoke<string>("get_cline_app_base_url").then(setAppBaseUrl);
}, []);

// View-level: central builder for all env-dependent links
const buildAccountUrl = (path: string) => {
  if (!appBaseUrl) return undefined; // hide/disable until resolved
  return new URL(path, appBaseUrl).toString();
};

const dashboardUrl = buildAccountUrl("/dashboard");
const privacyUrl = buildAccountUrl("/privacy");
```

Result: links stay consistent across environments, configuration is loaded with the right lifecycle, and account-derived data isn’t unnecessarily synchronized through global state.