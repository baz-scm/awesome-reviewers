---
title: Config resolution precedence
description: Configuration values (CLI flags, environment variables, provider/runtime
  overrides, computed defaults) must be resolved through one well-defined precedence
  chain, and that resolution must happen once, at the right scope, with the result
  reused everywhere instead of being recomputed independently in different code paths.
repository: cline/cline?ref=main
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 70980
---

Configuration values (CLI flags, environment variables, provider/runtime overrides, computed defaults) must be resolved through one well-defined precedence chain, and that resolution must happen once, at the right scope, with the result reused everywhere instead of being recomputed independently in different code paths.

Guidelines:
- Define and document an explicit precedence order, e.g. explicit caller option > subcommand flag > root/global flag > environment variable > computed default, and make every option-reading site consistent with it. Be careful with negatable flags (e.g. `--no-mouse`): read `getOptionValueSource(...)` rather than the raw boolean, since the flag parser will otherwise default the value to `true`/`false` and silently clobber the env-var fallback.
```ts
const authMouse =
  (authCmd.getOptionValueSource("mouse") === "cli" ? authCmd.opts().mouse : undefined) ??
  (program.getOptionValueSource("mouse") === "cli" ? program.opts().mouse : undefined);
// later, inside the consumer:
const useMouse = input.mouse !== undefined
  ? input.mouse
  : process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0";
```
- When a value derives a default for another option (e.g. `allowBindFallback: !hasExplicitEndpoint`), always let an explicitly supplied value win: `allowBindFallback ?? !hasExplicitEndpoint`, never let the derived default silently override a caller's explicit choice.
- Resolve environment-dependent values (base URLs, backend endpoints, app links) once from the single source of truth that other calls already use, and derive everything else from that same resolved value — don't let one code path read a raw env/config override while another reads a different default, which causes links or requests to point at the wrong environment. If startup doesn't support switching environments mid-session, resolve once at startup and pass the resolved value down rather than re-deriving it on every call.
- When an environment- or backend-derived value has no match (e.g. a proxy/self-hosted backend with no known app URL), fail safe by omitting the dependent feature rather than guessing another environment.
- Choose default values (timeouts, retry windows, etc.) empirically from telemetry/data covering all platforms/clients that share the same code path, and keep a single default unless there's a clear platform-specific reason and data to justify diverging — don't let one client's edge case push a shared default past constraints other clients depend on.

Applying this consistently prevents configuration drift between related code paths and makes precedence between flags, env vars, and defaults predictable and testable.</description>
</invoke>
