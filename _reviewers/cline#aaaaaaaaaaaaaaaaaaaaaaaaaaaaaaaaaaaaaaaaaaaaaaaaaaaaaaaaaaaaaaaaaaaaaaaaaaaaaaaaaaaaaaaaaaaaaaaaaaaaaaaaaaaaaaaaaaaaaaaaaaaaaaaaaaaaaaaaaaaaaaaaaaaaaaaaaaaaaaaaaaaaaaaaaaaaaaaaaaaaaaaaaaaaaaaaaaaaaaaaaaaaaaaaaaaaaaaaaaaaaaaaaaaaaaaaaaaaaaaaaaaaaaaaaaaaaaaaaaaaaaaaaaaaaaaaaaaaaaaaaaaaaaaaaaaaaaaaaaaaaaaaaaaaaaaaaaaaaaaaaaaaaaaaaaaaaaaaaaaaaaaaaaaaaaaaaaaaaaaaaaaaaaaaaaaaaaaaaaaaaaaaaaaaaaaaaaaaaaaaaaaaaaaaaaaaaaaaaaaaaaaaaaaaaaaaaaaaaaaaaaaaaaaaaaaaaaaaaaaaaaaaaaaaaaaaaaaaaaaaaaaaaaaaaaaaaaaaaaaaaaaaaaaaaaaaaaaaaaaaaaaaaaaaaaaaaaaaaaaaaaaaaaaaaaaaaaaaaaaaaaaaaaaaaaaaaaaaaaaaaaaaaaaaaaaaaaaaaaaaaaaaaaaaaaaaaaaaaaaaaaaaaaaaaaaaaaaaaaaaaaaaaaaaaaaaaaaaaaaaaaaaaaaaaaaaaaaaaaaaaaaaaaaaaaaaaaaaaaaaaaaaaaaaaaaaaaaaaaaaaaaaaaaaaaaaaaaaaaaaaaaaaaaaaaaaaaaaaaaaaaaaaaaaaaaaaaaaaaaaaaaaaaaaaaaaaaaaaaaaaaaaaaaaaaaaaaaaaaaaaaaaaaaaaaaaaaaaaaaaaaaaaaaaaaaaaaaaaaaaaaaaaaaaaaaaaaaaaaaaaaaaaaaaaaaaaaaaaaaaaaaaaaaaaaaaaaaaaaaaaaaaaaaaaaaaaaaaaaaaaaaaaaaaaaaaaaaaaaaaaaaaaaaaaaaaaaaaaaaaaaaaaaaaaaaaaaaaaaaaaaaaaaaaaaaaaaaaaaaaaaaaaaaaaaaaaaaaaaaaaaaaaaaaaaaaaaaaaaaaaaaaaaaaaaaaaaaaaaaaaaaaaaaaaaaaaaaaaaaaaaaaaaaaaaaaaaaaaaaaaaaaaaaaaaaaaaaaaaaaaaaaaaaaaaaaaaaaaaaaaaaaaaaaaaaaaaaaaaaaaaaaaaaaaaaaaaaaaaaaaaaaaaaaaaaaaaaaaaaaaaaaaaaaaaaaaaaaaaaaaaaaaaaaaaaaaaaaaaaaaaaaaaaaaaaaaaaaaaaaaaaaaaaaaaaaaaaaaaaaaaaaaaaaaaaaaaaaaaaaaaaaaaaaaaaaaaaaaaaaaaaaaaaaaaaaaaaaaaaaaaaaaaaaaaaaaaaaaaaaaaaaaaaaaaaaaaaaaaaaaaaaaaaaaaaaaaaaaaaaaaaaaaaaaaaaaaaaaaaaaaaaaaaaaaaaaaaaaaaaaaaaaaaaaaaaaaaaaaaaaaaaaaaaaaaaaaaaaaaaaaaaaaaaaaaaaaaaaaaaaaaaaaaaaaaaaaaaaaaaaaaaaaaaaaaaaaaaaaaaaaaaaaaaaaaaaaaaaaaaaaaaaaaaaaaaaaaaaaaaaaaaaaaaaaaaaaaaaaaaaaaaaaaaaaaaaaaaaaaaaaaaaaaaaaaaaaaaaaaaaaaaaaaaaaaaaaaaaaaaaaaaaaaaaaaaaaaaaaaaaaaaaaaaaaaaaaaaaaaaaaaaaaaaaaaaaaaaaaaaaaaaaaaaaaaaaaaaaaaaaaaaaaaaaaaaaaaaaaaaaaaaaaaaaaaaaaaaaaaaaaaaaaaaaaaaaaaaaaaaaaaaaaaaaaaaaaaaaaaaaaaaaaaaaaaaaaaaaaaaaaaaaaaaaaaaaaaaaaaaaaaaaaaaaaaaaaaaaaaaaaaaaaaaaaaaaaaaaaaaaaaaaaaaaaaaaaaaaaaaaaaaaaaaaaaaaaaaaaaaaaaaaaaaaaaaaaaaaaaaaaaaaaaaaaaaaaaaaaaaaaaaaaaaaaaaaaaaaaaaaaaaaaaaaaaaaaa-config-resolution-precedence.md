---
title: Config resolution precedence
description: When a setting can come from multiple sources (CLI flags, environment
  variables, provider/account settings, or derived defaults), resolve it once at the
  earliest fixed point (e.g., process/session startup) and store the resolved value
  instead of re-deriving it on every call. If the environment/backend cannot change
  mid-session, there is no need for a...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 70973
---

When a setting can come from multiple sources (CLI flags, environment variables, provider/account settings, or derived defaults), resolve it once at the earliest fixed point (e.g., process/session startup) and store the resolved value instead of re-deriving it on every call. If the environment/backend cannot change mid-session, there is no need for a refresh lifecycle tied to unrelated events (e.g., account refresh); just compute it once and pass/cache it through context.

When layering sources, always let an explicit, caller-supplied value win over a computed or derived default, and check the actual option *source* rather than trusting a library's post-parsing default. For example, a negatable CLI flag like `--no-mouse` is defaulted to `true`/`false` by the parser even when the user never passed it, so reading the raw value would silently clobber an environment-variable fallback:

```ts
// Wrong: Commander's default for a negatable flag masks "not supplied"
const useMouse = opts.mouse ?? process.env.CLINE_MOUSE !== "0";

// Right: only treat it as explicit when the user actually passed it
const explicitMouse =
  cmd.getOptionValueSource("mouse") === "cli" ? cmd.opts().mouse : undefined;
const useMouse = explicitMouse ?? (process.env.CLINE_NO_MOUSE !== "1" && process.env.CLINE_MOUSE !== "0");
```

The same rule applies to options threaded through internal APIs: a caller-supplied override must take priority over a value derived elsewhere, expressed with `??` so the explicit value always wins:

```ts
// endpointOverrides.allowBindFallback is caller-supplied; only fall back
// to the endpoint-derived default when the caller didn't specify one.
allowBindFallback: endpointOverrides.allowBindFallback ?? !hasExplicitEndpoint,
```

Document and test the full precedence chain (explicit override → CLI flag → environment variable → computed default) end-to-end, including the "nothing was supplied" case, so defaulting logic in one layer cannot silently override a fallback intended for a lower layer.</description>
</invoke>
