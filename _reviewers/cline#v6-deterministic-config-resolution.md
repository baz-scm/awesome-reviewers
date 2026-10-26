---
title: Deterministic config resolution
description: When implementing configuration behavior (env vars, CLI flags, provider
  settings, frontmatter/config files), ensure the code follows a single, deterministic
  resolution path with explicit precedence and a consistent source of truth.
repository: cline/cline#v6
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 70864
---

When implementing configuration behavior (env vars, CLI flags, provider settings, frontmatter/config files), ensure the code follows a single, deterministic resolution path with explicit precedence and a consistent source of truth.

Apply these rules:
- **Unify resolution logic across components**: URLs/remotes/defaults/keys used for runtime actions must be resolved by the same helper/rules, not re-implemented differently.
- **Resolve once per lifecycle** when dynamic switching isn’t supported (e.g., startup). Pass the resolved values downstream rather than re-reading provider/env settings on every refresh/call.
- **Make precedence explicit and precedence-safe**:
  - Treat CLI options and env vars explicitly (don’t rely on library defaults that can clobber env fallbacks).
  - When a CLI flag supports negation (e.g., `--no-x`), confirm whether the value came from the CLI before using it.
- **Define and test parsing precedence** for config fields (e.g., `disabled` wins over legacy `enabled: false`; accept boolean variants consistently).
- **Use shared helpers for env/key detection** so onboarding/UI decisions match runtime behavior.
- **Keep tests isolated from the developer’s environment**: any probe/smoke tests that depend on config/discovery paths should override those paths inside the isolated temp home/session.

Example pattern (precedence-safe CLI/env):
```ts
function resolveMouse(input: { mouse?: boolean }, getOptionValueSource: (name: string) => string | undefined) {
  // Only trust CLI value if the option was actually provided by the user.
  const cliMouse = getOptionValueSource("mouse") === "cli" ? input.mouse : undefined;
  return cliMouse ?? (process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0");
}
```

Outcome: fewer mismatches (UI vs runtime, staging vs prod links, wrong model/keys/defaults), fewer “it works on my machine” config issues, and more predictable behavior across environments.