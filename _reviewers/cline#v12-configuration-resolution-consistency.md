---
title: Configuration resolution consistency
description: 'When multiple parts of the system depend on the same environment/provider
  configuration (links, onboarding eligibility, remotes, session behavior), treat
  configuration as “resolved truth”: derive it once using a shared helper/resolver,
  then pass the resolved value through. Do not re-resolve on every refresh unless
  the underlying backend/environment can...'
repository: cline/cline#v12
label: Configurations
language: TypeScript
comments_count: 6
repository_stars: 70872
---

When multiple parts of the system depend on the same environment/provider configuration (links, onboarding eligibility, remotes, session behavior), treat configuration as “resolved truth”: derive it once using a shared helper/resolver, then pass the resolved value through. Do not re-resolve on every refresh unless the underlying backend/environment can actually change.

Also enforce explicit precedence and avoid silent clobbering: if values can come from CLI flags, env vars, and defaults, use “value source” detection (not just the raw option value) so framework defaults (especially negatable flags) don’t override env.

Finally, prevent observers from mutating bootstrap/config identity that downstream logic uses (e.g., sessionId). Observability should attach hooks/telemetry, not change what core thinks the start state is.

Example patterns:
```ts
// 1) Resolve once and reuse (CLI/sidecar/webview)
const appBaseUrl = resolveClineAppBaseUrl(resolvedBackendBaseUrl /* computed once */);
return { privacySettingsUrl: appBaseUrl ? `${appBaseUrl}/...` : undefined };

// 2) Explicit precedence for CLI vs env (avoid Commander negatable default clobber)
const mouseFromCli = cmd.getOptionValueSource('mouse') === 'cli' ? cmd.opts().mouse : undefined;
const mouse = mouseFromCli ?? (process.env.CLINE_NO_MOUSE !== '1' && process.env.CLINE_MOUSE !== '0');

// 3) Observers must not rewrite bootstrap truth
function configure(input: CoreStartInput) {
  return { ...input /* unchanged */, hooks: attachHooks(input) }; // don’t set or infer sessionId here
}
```

Checklist for reviews:
- [ ] Is the same shared resolver/helper used everywhere for the same config concept?
- [ ] Is the resolved value computed once (startup) when the backend/env cannot change?
- [ ] When config sources compete, is precedence explicit and determined by source (not by framework defaults)?
- [ ] Do observers/configurers avoid mutating core bootstrap identifiers/state fields?
- [ ] Do tests isolate env/config so they don’t depend on developer machine settings?