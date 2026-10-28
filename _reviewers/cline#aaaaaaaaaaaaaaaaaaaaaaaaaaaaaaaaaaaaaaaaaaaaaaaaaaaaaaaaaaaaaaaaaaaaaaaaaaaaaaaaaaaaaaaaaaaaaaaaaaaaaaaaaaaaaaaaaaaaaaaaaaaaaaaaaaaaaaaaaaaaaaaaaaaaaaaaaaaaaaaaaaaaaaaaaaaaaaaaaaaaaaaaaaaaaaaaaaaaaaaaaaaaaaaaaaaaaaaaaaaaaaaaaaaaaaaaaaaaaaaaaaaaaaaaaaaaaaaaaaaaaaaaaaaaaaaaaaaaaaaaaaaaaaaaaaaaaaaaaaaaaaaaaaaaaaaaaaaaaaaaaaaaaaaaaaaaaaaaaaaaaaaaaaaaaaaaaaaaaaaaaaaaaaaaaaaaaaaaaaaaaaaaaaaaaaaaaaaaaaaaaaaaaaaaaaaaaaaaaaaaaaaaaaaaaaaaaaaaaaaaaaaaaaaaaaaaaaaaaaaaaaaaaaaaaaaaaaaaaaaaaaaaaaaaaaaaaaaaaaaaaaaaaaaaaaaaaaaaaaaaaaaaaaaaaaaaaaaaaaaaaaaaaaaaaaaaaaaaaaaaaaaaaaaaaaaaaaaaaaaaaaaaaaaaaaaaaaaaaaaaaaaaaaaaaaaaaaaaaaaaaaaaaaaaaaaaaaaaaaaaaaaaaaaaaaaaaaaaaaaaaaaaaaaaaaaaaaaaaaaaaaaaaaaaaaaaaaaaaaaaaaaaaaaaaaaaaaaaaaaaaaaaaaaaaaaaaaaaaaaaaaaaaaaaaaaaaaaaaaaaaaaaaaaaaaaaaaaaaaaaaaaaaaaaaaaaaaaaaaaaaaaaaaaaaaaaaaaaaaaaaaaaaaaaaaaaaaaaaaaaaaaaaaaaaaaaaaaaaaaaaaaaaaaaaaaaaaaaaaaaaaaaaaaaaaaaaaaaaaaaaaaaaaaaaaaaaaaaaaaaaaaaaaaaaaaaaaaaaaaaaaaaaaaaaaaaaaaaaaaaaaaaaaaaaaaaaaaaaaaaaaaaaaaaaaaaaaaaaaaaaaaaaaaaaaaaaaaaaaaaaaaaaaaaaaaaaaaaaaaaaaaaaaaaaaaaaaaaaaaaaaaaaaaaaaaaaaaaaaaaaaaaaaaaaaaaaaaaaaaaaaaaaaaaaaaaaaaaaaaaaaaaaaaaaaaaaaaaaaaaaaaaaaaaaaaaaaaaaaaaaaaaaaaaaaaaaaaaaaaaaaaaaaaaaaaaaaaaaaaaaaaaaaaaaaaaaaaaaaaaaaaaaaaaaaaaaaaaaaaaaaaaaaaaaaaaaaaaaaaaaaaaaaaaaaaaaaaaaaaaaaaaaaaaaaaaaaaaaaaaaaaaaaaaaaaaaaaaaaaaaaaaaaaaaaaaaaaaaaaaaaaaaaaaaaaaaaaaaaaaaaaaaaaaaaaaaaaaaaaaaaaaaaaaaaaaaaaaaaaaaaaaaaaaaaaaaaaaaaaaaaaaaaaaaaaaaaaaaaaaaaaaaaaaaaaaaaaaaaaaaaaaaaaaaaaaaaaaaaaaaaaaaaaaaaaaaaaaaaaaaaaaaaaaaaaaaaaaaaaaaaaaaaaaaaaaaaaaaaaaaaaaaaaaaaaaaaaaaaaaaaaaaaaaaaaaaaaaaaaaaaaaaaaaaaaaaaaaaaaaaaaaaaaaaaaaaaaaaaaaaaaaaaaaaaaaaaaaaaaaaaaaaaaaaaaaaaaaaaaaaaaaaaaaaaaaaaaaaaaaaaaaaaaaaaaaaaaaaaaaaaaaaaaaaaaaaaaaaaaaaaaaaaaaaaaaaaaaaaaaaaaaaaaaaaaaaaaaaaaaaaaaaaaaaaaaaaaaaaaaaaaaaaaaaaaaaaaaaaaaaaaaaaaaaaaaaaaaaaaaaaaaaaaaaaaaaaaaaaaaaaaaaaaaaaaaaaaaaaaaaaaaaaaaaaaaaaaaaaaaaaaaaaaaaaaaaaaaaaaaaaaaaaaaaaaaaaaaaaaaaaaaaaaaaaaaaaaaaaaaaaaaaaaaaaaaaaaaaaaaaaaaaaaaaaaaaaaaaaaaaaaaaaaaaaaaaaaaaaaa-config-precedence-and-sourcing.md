---
title: Config precedence and sourcing
description: When a setting can come from more than one place (CLI flag, environment
  variable, persisted config, provider/environment manifest, derived default), define
  an explicit precedence order, document it, and test every combination — don't let
  implicit library defaults silently win.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 70965
---

When a setting can come from more than one place (CLI flag, environment variable, persisted config, provider/environment manifest, derived default), define an explicit precedence order, document it, and test every combination — don't let implicit library defaults silently win.

Concretely:
- Pick one precedence order per setting (e.g., explicit CLI flag > environment variable > manifest-provided default > hardcoded fallback) and apply it consistently. Don't read a raw option value if the underlying library injects an implicit default for it: e.g. Commander defaults a negatable `--no-mouse` flag to `true`, so resolving it must check `getOptionValueSource(...) === "cli"` before falling back to an env var, otherwise the "unset" case is indistinguishable from an explicit `--mouse`:
```ts
const mouse =
	(cmd.getOptionValueSource("mouse") === "cli" ? cmd.opts().mouse : undefined) ??
	(process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0");
```
- When a caller can explicitly pass an option that also has a derived/computed default (e.g. a feature flag derived from "is there an explicit endpoint"), make the caller-supplied value win outright and use the derived value only as the `??` fallback, not the other way around.
- Resolve environment- or provider-specific values (base URLs, default model IDs, etc.) from one authoritative source instead of re-deriving them independently in each consumer. Two places that each read "the same" setting from different inputs (e.g. one reading the provider's configured `baseUrl`, another reading a separate `appBaseUrl`/environment variable) will eventually disagree; instead, resolve once and derive everything else from that single resolved value, falling back to "disabled/hidden" when nothing matches rather than guessing.
- Avoid hardcoded last-resort literals that are wrong for anything but the common case (e.g. a single hardcoded model id used as the fallback for every provider); pull the default from the relevant config/manifest first, skip placeholder values, and only fall back to a global constant when the manifest has nothing usable.
- Add a test per source/precedence combination (flag only, env only, both, neither) so the resolution logic doesn't silently regress.